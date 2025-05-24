
from yakoon.engine.core.registry import DomainRegistry
from yakoon.engine.settings import Settings
from yakoon.engine.core.parser import Request
from yakoon.engine.core.dialog.manager import DialogManager
from yakoon.engine.core.tools.command_tool import split_batch_input
from yakoon.engine.services.log_service import LogService
from yakoon.engine.system.context import Context
from yakoon.engine.system.session import BaseSession, PrintError, PrintMessage


class Engine():
     
   def __init__(self, registry: DomainRegistry):
      """
      Creates a new instance of the class engine.
      """
      self._registry = registry

   @property
   def registry(self) -> DomainRegistry:
        return self._registry

   async def send(self, session_id: str, input_str: str, on_msg: PrintMessage, on_err: PrintError, depth=0):   
      """
      Entry point for any user input.
      Handles session lifecycle, context binding, output routing, and optional batch execution.
      """
      if depth > Settings.max_dispatch_depth:
        return await on_err("Command recursion limit reached.")

      inputs = split_batch_input(input_str) if Settings.enable_batch else [input_str]

      session, _ = await self.registry.sessions.get_or_create(session_id)
      session.bind_context(Context(self)) 

      groups = set()
      session.command_groups = []
      for controller in self.registry.controllers + [self.registry.system]:
         groups.update(controller.get_default_command_groups_with_prefix())
      session.command_groups = list(groups)
   
      session.out = on_msg
      session.err = on_err

      await self.registry.system.on_before_send(session)
      for raw in inputs:
         await self._send_one(session, raw.strip())
      await self.registry.system.on_after_send(session)
         
   async def _send_one(self, session: BaseSession, input_str: str):   
      if DialogManager.is_waiting_to_handle(session.id, input_str):
         return

      request = Request(input_str)
      if not request.cmd:
         return await session.err("Kein Befehl erkannt.")
      
      result = self._registry.resolve(request.cmd, session)
      if not result:
         return await session.err(f"Befehl '{request.cmd}' nicht gefunden.")

      controller, command = result
      session.ctx.bind_controller(controller) 

      try:
         await controller.on_before_run_command(session, request, command)
         await command.run(session, request)
         await controller.on_after_run_command(session, request, command)

      except PermissionError as exc:
         LogService.permission(session, "command", command.key)
         await session.err(str(exc))

      except ValueError as exc:
         await session.err(str(exc))

      except Exception as exc:
         await session.err("Ein interner Fehler ist aufgetreten.")
         LogService.error(exc)