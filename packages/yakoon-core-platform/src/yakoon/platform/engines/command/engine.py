import asyncio
from collections import deque
from typing import Optional, Tuple

from yakoon.base.ports import AuditLogService
from yakoon.base.models.key import Key
from yakoon.base.commands.request import Request
from yakoon.base.controllers.base import BaseController
from yakoon.base.runtime.session.output import Output
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
   
   async def initialize(self, io: Output):           
      session = Session(None)      
      
      # Bind the given Output to this session for output and error handling.
      session.bind_io(io)

      ## initialize the controllers
      for controller in self._directory.get_all():
         if hasattr(controller, "on_initialize"):
            await controller.on_initialize(session)

   async def _find_matching_command(
         self, active_router_id, request: Request, 
         session: Session) -> Optional[Tuple[BaseController, Command]]:
      
      # Include the session-local command group for dynamic routing.
      # This allows commands (e.g. exits or context actions) to be registered
      cmd_groups = session.cmd_groups + session.cmd_groups_dynamic
      cmd_groups += ["office.mailing:system", "auth:system"] # TODO
           
      find = self._commands.find
      result: tuple[str, Command] = find(active_router_id, request.command(), cmd_groups)
      if result:
         active_router_id, command = result
         return self._directory.get(active_router_id), command

   async def invoke_text(self, session: Session, input_str: str):
      result = await self.resolve_task(session, input_str)
      return result

   async def dispatch(self, session_key: Key, input_str: str, io: Output) -> Session:
      shell = self._directory.find_shell()
      session: Session = await shell.on_resolve_session(session_key)

      session.bind_io(io)
      if not session.get_active_controller():
         session.set_active_controller(shell.id)

      return await self.resolve_task(session, input_str)

   async def resolve_task(self, session: Session, input_str: str) -> Session:
      skey = str(session.key)

      # 1) Prompt response path
      if DialogManager.is_waiting(session):
         DialogManager.resolve_prompt(session, input_str)

         # Drive the existing active task until it either finishes or asks again
         await self._drive_until_blocked_or_done(session)

         # One consistent end-of-dispatch yield (same as normal path)
         await asyncio.sleep(0)
         #print("DISPATCH END")
         return session

      # 2) Normal command path
      task = asyncio.create_task(self._run_one(session, input_str))
      self._active_tasks[skey] = task

      await self._drive_until_blocked_or_done(session)

      await asyncio.sleep(0)
      #print("DISPATCH END")
      return session

   async def _drive_until_blocked_or_done(self, session: Session):
      task = self._active_tasks.get(str(session.key))
      if not task:
         return

      # Lass den Command weiterlaufen, bis:
      # - fertig ODER
      # - er erneut promptet
      while not task.done() and not DialogManager.is_waiting(session):
         await asyncio.sleep(0)

      if task.done():
        self._active_tasks.pop(str(session.key), None)

   async def _run_one(self, session: Session, raw: str) -> bool:
      shell = self._directory.find_shell()
      try:
         await shell.on_shell_validate(session)
         return await self._send_one(session, raw)
      finally:
         await shell.on_shell_finalize(session)

   async def _send_one(self, session: Session, input_str: str) -> bool:  

      ok = True
      active_router_id = session.get_active_controller()
      command, request = None, Request(input_str)
      if not request.command():
         return  #return await session.fail("Kein Befehl erkannt.")

      try:
         if active_router_id:
            # Domain-level hook before resolving the input into a command.
            # Allows dynamic command registration or early input rewriting.
            controller = self._directory.get(active_router_id)
            if controller: # TODO: proxy.on_before_resolve -> dieser löst das intern auf (controller oder websocket)
               await controller.on_before_resolve(session)

         # resolve the commands
         result = await self._find_matching_command(active_router_id, request, session)
         if not result:
            raise CmdNotFound(f"{request.command()}")

         controller, command = result
         command.controller = controller
                  
         # Pre-command hook: modify or validate request before execution
         await controller.on_before_run_command(session, request, command)
         
         # Main command execution
         await command.run(session, request)

         # Post-command hook: cleanup, logging, side effects
         await controller.on_after_run_command(session, request, command)

      except CmdNotFound as exc:
         ok = False
         await session.fail(f"Unbekannter Befehl: '{request.command()}'")

      except PermissionError as exc:
         ok = False
         audit = self._services.get(AuditLogService)
         await audit.permission(session, "command", command.key)
         await session.fail(str(exc))

      except ValueError as exc:
         ok = False
         await session.fail(str(exc))

      except Exception as exc:
         ok = False
         audit = self._services.get(AuditLogService)
         await audit.error(exc)
         await session.fail("Ein interner Fehler ist aufgetreten.")

      finally:       
         if command: 
            command.controller = None
         if active_router_id:
            # Hook called when a domain session is about to end.
            # Used for cleanup of runtime data, disconnection, or persistence.   
            controller = self._directory.get(active_router_id)
            if controller:
               await controller.on_cleanup(session)

      return ok