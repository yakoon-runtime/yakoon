import asyncio
from collections import deque
from typing import Optional, Tuple

from yakoon.base.commands.request import Request
from yakoon.base.controllers.base import BaseController
from yakoon.base.models.key import Key
from yakoon.base.runtime.dialogs.manager import DialogManager
from yakoon.base.runtime.session.output import Output
from yakoon.base.runtime.session import Session
from yakoon.base.commands.command import CmdNotFound, Command

from yakoon.base.runtime.system.registry import ServiceRegistry
from yakoon.platform.engines.command.router import CommandDirectory
from yakoon.platform.settings import settings
from yakoon.platform.controllers.directory import ControllerDirectory
from yakoon.platform.engines.command.batch import split_batch_input


class Engine:
     
   def __init__(self, 
                directory: ControllerDirectory, 
                services: ServiceRegistry, 
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
      for controller in await self._directory.get_all_for():
         if hasattr(controller, "on_initialize"):
            await controller.on_initialize(session)
    
   async def _resolve_for_controller(
         self, controller_id, request: Request, 
         session: Session) -> Optional[Tuple[BaseController, Command]]:
      
      # Include the session-local command group for dynamic routing.
      # This allows commands (e.g. exits or context actions) to be registered
      cmd_groups = session.cmd_groups + session.cmd_groups_dynamic
      
      result: tuple[str, Command] = await self._commands.resolve(request.cmd, cmd_groups)
      if result:
         controller_id, command = result
         return await self._directory.get(controller_id), command

   
   async def dispatch(self, session_key: Key, input_str: str, io: Output):   
      """
      Entry point for any user input.
      Handles session lifecycle, context binding, output routing, and optional batch execution.
      """
      gateway = await self._directory.get_gateway()
      session = await gateway.on_resolve_session(session_key)
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
         gateway = await self._directory.get_gateway()
         try:
            await gateway.on_gateway_validate(session)
            await self._send_one(session, raw)
         finally:
            # Final platform-level hook after command execution.
            # Used for post-processing, logging, or global session update
            await gateway.on_gateway_finalize(session)

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

      command, request = None, Request(input_str)
      if not request.cmd:
         return await session.fail("Kein Befehl erkannt.")

      domain_id = session.ctx("gateway", "domain_id", persist=True)
      domain_id = "mesh"

      try:
         if domain_id:
            # Domain-level hook before resolving the input into a command.
            # Allows dynamic command registration or early input rewriting.
            controller = await self._directory.get(domain_id)
            if controller: # TODO: proxy.on_before_resolve -> dieser löst das intern auf (controller oder websocket)
               await controller.on_before_resolve(session)

         # resolve the commands
         result = await self._resolve_for_controller(domain_id, request, session)
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
         audit = await self._services.get("audit")
         await audit.permission(session, "command", command.key)
         await session.fail(str(exc))

      except ValueError as exc:
         await session.fail(str(exc))

      except Exception as exc:
         audit = await self._services.get("audit")
         await audit.error(exc)
         await session.fail("Ein interner Fehler ist aufgetreten.")

      finally:       
         if command: 
            command.controller = None
         if domain_id:
            # Hook called when a domain session is about to end.
            # Used for cleanup of runtime data, disconnection, or persistence.   
            controller = await self._directory.get(domain_id)
            if controller:
               await controller.on_cleanup(session)

