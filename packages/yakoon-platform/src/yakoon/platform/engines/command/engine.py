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

from yakoon.platform.settings import settings
from yakoon.base.directories.service import ServiceDirectory
from yakoon.platform.runtime.dialogs.manager import DialogManager
from yakoon.platform.engines.command.router import CommandDirectory
from yakoon.platform.directories.controller import ControllerDirectory
from yakoon.platform.engines.command.batch import split_batch_input


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
      cmd_groups += ["office.mailing:system"] # TODO
      
      find = self._commands.find
      result: tuple[str, Command] = find(active_router_id, request.cmd, cmd_groups)
      if result:
         active_router_id, command = result
         return self._directory.get(active_router_id), command

   
   async def dispatch(self, session_key: Key, input_str: str, io: Output):   
      """
      Entry point for any user input.
      Handles session lifecycle, context binding, output routing, and optional batch execution.
      """
      shell = self._directory.find_shell()
      session = await shell.on_resolve_session(session_key)
      session.bind_io(io)

      inputs = split_batch_input(input_str) if settings.engine.enable_batch else [input_str]  
      await asyncio.create_task(self._run_processing(session, inputs))

   async def _run_processing(self, session: Session, inputs: list[str]):
      """
      Executes a batch of commands sequentially, including prompt handling.

      - Each command runs in an isolated task to allow blocking prompts via `ask()`.
      - If a prompt is triggered during execution, the next item in the queue is automatically
         used to resolve it (via `DialogManager.resolve_prompt()`).
      - If no further input is available when a prompt is active, execution stops.
      - The final input in the batch can be interpreted as a prompt response if needed.

      Args:
         session (BaseSession): The session context in which the batch runs.
         inputs (list[str]): A list of commands and/or prompt responses.
      """
      queue = deque(inputs)

      async def _run_internal_task(raw):
         # Platform-level pre-processing hook before input parsing.
         # Used to validate or prepare the session (e.g., locale, account, command set).
         shell = self._directory.find_shell()
         try:
            await shell.on_shell_validate(session)
            await self._send_one(session, raw)
         finally:
            # Final platform-level hook after command execution.
            # Used for post-processing, logging, or global session update
            await shell.on_shell_finalize(session)

      while queue:
         await asyncio.sleep(0.01)  # yield control briefly
         raw = queue.popleft()

         # If this is the final input and a prompt is active → treat it as the response
         if raw and not queue:
            if DialogManager.is_waiting(session.key):
               DialogManager.resolve_prompt(session.key, raw)
               return

         task = asyncio.create_task(_run_internal_task(raw))

         while not task.done():
            await asyncio.sleep(0.01)

            if DialogManager.is_waiting(session.key):
               if queue:
                  next_raw = queue.popleft()
                  DialogManager.resolve_prompt(session.key, next_raw)
                  break  # prompt resolved, allow task to continue
               else:                   
                  return # Prompt expected, but no further input in batch 

   async def _send_one(self, session: Session, input_str: str):   

      active_router_id = session.get_active_controller()
      command, request = None, Request(input_str)
      if not request.cmd:
         return await session.fail("Kein Befehl erkannt.")

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
            raise CmdNotFound(f"{request.cmd}")

         controller, command = result
         command.controller = controller
                  
         # Pre-command hook: modify or validate request before execution
         await controller.on_before_run_command(session, request, command)
         
         # Main command execution
         await command.run(session, request)

         # Post-command hook: cleanup, logging, side effects
         await controller.on_after_run_command(session, request, command)

      except CmdNotFound as exc:
         await session.fail(f"Unbekannter Befehl: '{request.cmd}'")

      except PermissionError as exc:
         audit = self._services.get(AuditLogService)
         await audit.permission(session, "command", command.key)
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
         if active_router_id:
            # Hook called when a domain session is about to end.
            # Used for cleanup of runtime data, disconnection, or persistence.   
            controller = self._directory.get(active_router_id)
            if controller:
               await controller.on_cleanup(session)

