import asyncio
from typing import Optional, Tuple

from yakoon.base.models.input import DispatchInput
from yakoon.base.models.perm import PermBit
from yakoon.base.ports import AuditLogService, CommandQueueService, DialogService, PermissionService
from yakoon.base.commands.request import Request
from yakoon.base.controllers.base import BaseController
from yakoon.base.runtime.session import Session
from yakoon.base.commands.command import CmdNotFound, Command
from yakoon.base.directories.service import ServiceDirectory

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
         self, active_router_id, request: Request) -> Optional[Tuple[BaseController, Command]]:
      
      find = self._commands.find
      result: tuple[str, Command] = find(active_router_id, request.command())
      if result:
         active_router_id, command = result
         return self._directory.get(active_router_id), command

   async def dispatch(self, session: Session, di: DispatchInput) -> Session:

      skey = str(session.key)
      shell = self._directory.find_shell()
      if not session.get_active_controller():
         session.set_active_controller(shell.id)

      # 1) Prompt response path
      dialog_service = self.services.get(DialogService)
      if dialog_service.is_waiting(session):
         dialog_service.resolve_prompt(session, di.command)

         # Drive the existing active task until it either finishes or asks again
         await self._drive_until_blocked_or_done(session)

         #print("DISPATCH END")
         return session

      # 2) Normal command path
      loop = asyncio.get_running_loop()
      task = loop.create_task(self._dispatch_command(session, di))

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
      dialog_service = self.services.get(DialogService)
      while not task.done() and not dialog_service.is_waiting(session):
         await asyncio.sleep(0.005)

      if task.done():
        _ = task.exception()  # drain
        self._active_tasks.pop(str(session.key), None)

   async def _dispatch_command(self, session: Session, di: DispatchInput) -> bool:
      failed = False
      request = Request(di.command)

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
         result = await self._find_matching_command(controller_id, request)
         if not result:
               raise CmdNotFound(f"{request.command()}")

         resolved_controller, command = result

         perm_service = self.services.get(PermissionService)
         fq = f"{resolved_controller.id}:{command.key}"
         if not perm_service.can_execute(session, fq):
            raise PermissionError("Permission denied")

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
         failed = True
         await session.fail(f"{request.command()}': command not found... use 'man'")

      except PermissionError as exc:
         failed = True
         audit = self._services.get(AuditLogService)
         # command may be None if permission fails early
         await audit.permission(session, "command", command.key if command else request.command())
         await session.fail(str(exc))

      except ValueError as exc:
         failed = True
         await session.fail(str(exc))

      except Exception as exc:
         failed = True
         audit = self._services.get(AuditLogService)
         await audit.error(exc)
         await session.fail("Ein interner Fehler ist aufgetreten.")

      finally:
         if command:
               command.controller = None

         if failed and di.batch_id:
            queue = self._services.get(CommandQueueService)
            queue.cancel_batch(session, di.batch_id)

         # Policy 2: cleanup the controller that executed this command
         # (NOT the current active controller after the command potentially changed it)
         await controller.on_cleanup(session)