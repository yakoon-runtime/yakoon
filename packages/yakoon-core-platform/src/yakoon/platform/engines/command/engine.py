import asyncio
from typing import Optional, Tuple

from yakoon.base.ports import AuditLogService
from yakoon.base.commands.request import Request
from yakoon.base.controllers.base import BaseController
from yakoon.base.runtime.session import Session
from yakoon.base.commands.command import CmdNotFound, Command
from yakoon.base.directories.service import ServiceDirectory

from yakoon.platform.runtime.dialogs.manager import DialogManager
from yakoon.platform.engines.command.router import CommandDirectory
from yakoon.platform.directories.controller import ControllerDirectory


class Engine:
     
   def __init__(self, 
                directory: ControllerDirectory, 
                services: ServiceDirectory, 
                commands: CommandDirectory):
      """      
      Creates a new instance of the class engine.
      """
      self._directory = directory
      self._services = services
      self._commands = commands
      self._active_tasks: dict[str, asyncio.Task] = {}
   
   @property
   def services(self) -> ServiceDirectory:
        return self._services

   async def _find_matching_command(
         self, active_router_id, request: Request, 
         session: Session) -> Optional[Tuple[BaseController, Command]]:
      
      cmd_groups = list(session.allowed_command_groups)

      find = self._commands.find
      result: tuple[str, Command] = find(active_router_id, request.command(), cmd_groups)
      if result:
         active_router_id, command = result
         return self._directory.get(active_router_id), command

   async def dispatch(self, session: Session, input_str: str) -> Session:

      skey = str(session.key)
      shell = self._directory.find_shell()
      if not session.get_active_controller():
         session.set_active_controller(shell.id)

      # 1) Prompt response path
      if DialogManager.is_waiting(session):
         DialogManager.resolve_prompt(session, input_str)

         # Drive the existing active task until it either finishes or asks again
         await self._drive_until_blocked_or_done(session)

         #print("DISPATCH END")
         return session

      # 2) Normal command path
      task = asyncio.create_task(self._dispatch_command(session, input_str))
      self._active_tasks[skey] = task

      await self._drive_until_blocked_or_done(session)
      return session

   async def _drive_until_blocked_or_done(self, session: Session):
      task = self._active_tasks.get(str(session.key))
      if not task:
         return

      # Lass den Command weiterlaufen, bis:
      # - fertig ODER
      # - er erneut promptet
      while not task.done() and not DialogManager.is_waiting(session):
         await asyncio.sleep(0.005)

      if task.done():
        _ = task.exception()  # drain
        self._active_tasks.pop(str(session.key), None)

   async def _dispatch_command(self, session: Session, input_str: str) -> bool:
      request = Request(input_str)

      # Empty input -> noop (or fail, depending on your UX choice)
      if not request.command():
         return True

      # Active controller is the single routing context (S1)
      controller_id = session.get_active_controller()
      controller = self._directory.get(controller_id) if controller_id else None
      if not controller:
         await session.fail("Kein aktiver Controller gesetzt.")
         return False

      command = None

      try:
         # Domain-level hook before resolving the input into a command.
         # Allows dynamic command registration or early input rewriting.
         await controller.on_before_resolve(session)

         # Resolve command within the single active controller context (+ groups)
         result = await self._find_matching_command(controller_id, request, session)
         if not result:
               raise CmdNotFound(f"{request.command()}")

         resolved_controller, command = result

         # Safety: Under S1, resolved controller should match active controller
         # (If your router can return a different controller, keep this; otherwise you can drop it.)
         controller = resolved_controller

         command.controller = controller

         # Pre-command hook
         await controller.on_before_run_command(session, request, command)

         # Execute command
         await command.run(session, request)

         # Post-command hook
         await controller.on_after_run_command(session, request, command)

      except CmdNotFound:
         await session.fail(f"{request.command()}': command not found... use 'man'")

      except PermissionError as exc:
         audit = self._services.get(AuditLogService)
         # command may be None if permission fails early
         await audit.permission(session, "command", command.key if command else request.command())
         await session.fail(str(exc))

      except ValueError as exc:
         await session.fail(str(exc))

      except Exception as exc:
         audit = self._services.get(AuditLogService)
         await audit.error(exc)
         await session.fail("Ein interner Fehler ist aufgetreten.")

      finally:
         if command:
               command.controller = None

         # Policy 2: cleanup the controller that executed this command
         # (NOT the current active controller after the command potentially changed it)
         await controller.on_cleanup(session)