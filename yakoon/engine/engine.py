
import asyncio
from collections import deque
from yakoon.core.parser import Request
from yakoon.engine.io.output import Output
from yakoon.engine.registry import DomainRegistry
from yakoon.engine.settings import Settings
from yakoon.engine.batch import split_batch_input
from yakoon.runtime.models.session import BaseSession
from yakoon.runtime.dialogs.manager import DialogManager
from yakoon.services.core.log import LogService
from yakoon.services.registry import SessionServiceRegistry


class Engine():
     
   def __init__(self, registry: DomainRegistry):
      """      
      Creates a new instance of the class engine.
      """
      self._registry = registry

   @property
   def registry(self) -> DomainRegistry:
        return self._registry
   
   async def initialize(self, io: Output):           
      session = BaseSession(None)      
      
      # Bind the given Output to this session for output and error handling.
      session.bind_io(io)

      for controller in self._registry.get_controllers():
         if hasattr(controller, "on_initialize"):
            await controller.on_initialize(session)

   async def _require_registry_with_session(self, bucket: str) -> SessionServiceRegistry :
      registry = await self.registry.get_gateway().service_router.get_registry(bucket)
      if not isinstance(registry, SessionServiceRegistry):
         raise RuntimeError(f"Registry for bucket '{bucket}' does not provide session services")
      if not registry:
         raise RuntimeError(f"No ServiceRegistry found for bucket: {bucket}")
      return registry                                

   async def dispatch(self, session_id: str, input_str: str, io: Output):   
      """
      Entry point for any user input.
      Handles session lifecycle, context binding, output routing, and optional batch execution.
      """
      inputs = split_batch_input(input_str) if Settings.enable_batch else [input_str]
      
      services = await self._require_registry_with_session("gateway")      
      session, _ = await services.sessions.get_or_create(session_id)

      # Bind the given Output to this session for output and error handling.
      session.bind_io(io)

      await asyncio.create_task(self._run_processing(session, inputs))

   async def _run_processing(self, session: BaseSession, inputs: list[str]):
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
         await self._registry.get_gateway().on_gateway_validate(session)

         try:
            await self._send_one(session, raw)
         finally:
            # Final platform-level hook after command execution.
            # Used for post-processing, logging, or global session update
            await self._registry.get_gateway().on_gateway_finalize(session)

      while queue:
         await asyncio.sleep(0.01)  # yield control briefly
         raw = queue.popleft()

         # If this is the final input and a prompt is active → treat it as the response
         if raw and not queue:
            if DialogManager.is_waiting(session.id):
               DialogManager.resolve_prompt(session.id, raw)
               return

         task = asyncio.create_task(_run_internal_task(raw))

         while not task.done():
            await asyncio.sleep(0.01)

            if DialogManager.is_waiting(session.id):
               if queue:
                  next_raw = queue.popleft()
                  DialogManager.resolve_prompt(session.id, next_raw)
                  break  # prompt resolved, allow task to continue
               else:                   
                  return # Prompt expected, but no further input in batch 

   async def _send_one(self, session: BaseSession, input_str: str):   

      command = None
      request = Request(input_str)
      if not request.cmd:
         return await session.fail("Kein Befehl erkannt.")

      try:
         if session.domain_id:
            # Domain-level hook before resolving the input into a command.
            # Allows dynamic command registration or early input rewriting.
            current = self._registry.get_controller_by_id(session.domain_id)
            await current.on_before_resolve(session)

         # resolve the commands
         result = self._registry.resolve(request.cmd, session)
         if not result:
            return await session.fail(f"Befehl '{request.cmd}' nicht gefunden.")

         controller, command = result
         command.controller = controller
                  
         # Pre-command hook: modify or validate request before execution
         await controller.on_before_run_command(session, request, command)
         
         # Main command execution
         await command.run(session, request)
         
         # Post-command hook: cleanup, logging, side effects
         await controller.on_after_run_command(session, request, command)

      except PermissionError as exc:
         LogService.permission(session, "command", command.key)
         await session.fail(str(exc))

      except ValueError as exc:
         await session.fail(str(exc))

      except Exception as exc:
         await session.fail("Ein interner Fehler ist aufgetreten.")
         LogService.error(exc)

      finally:       
         if command: 
            command.controller = None
         if session.domain_id:
            # Hook called when a domain session is about to end.
            # Used for cleanup of runtime data, disconnection, or persistence.   
            current = self._registry.get_controller_by_id(session.domain_id)
            await current.on_cleanup(session)
