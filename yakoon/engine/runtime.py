
from yakoon.engine.settings import Settings
from yakoon.engine.core.parser import Request
from yakoon.engine.core.dialog.manager import DialogManager
from yakoon.engine.core.domain.definition import DomainDefinition
from yakoon.engine.core.router import CommandRouter
from yakoon.engine.core.tools.command_tool import split_batch_input
from yakoon.engine.services.log_service import LogService
from yakoon.engine.system.session import (
   BaseSession, OnGetSession, PrintError, PrintMessage, Sessions)


class Engine():
     
   def __init__(self, domain_def: DomainDefinition):
      """
      Creates a new instance of the class engine.
      """
      self._domain = domain_def()
      self._sessions = Sessions(self)
      self._router = CommandRouter()
      for commands_set in domain_def.commandsets:
         mode = getattr(commands_set, "mode", "system")
         self._router.register(mode, commands_set)

   @property
   def router(self) -> CommandRouter:
        return self._router

   async def enter(self, session_id: str,
                   on_print_msg: PrintMessage,
                   on_print_err: PrintError,
                   on_ready: OnGetSession):      

      async def _on_ready_internal(session: BaseSession):
         session.out = on_print_msg
         session.err = on_print_err
         await on_ready(session)

      async def _on_create_new(session: BaseSession):
         session.command_groups = self._domain.default_command_groups or []
         await _on_ready_internal(session)
       
      await self._sessions.create_session(
         session_id, _on_create_new, _on_ready_internal)

   async def send(self, session: BaseSession, input_str: str):   
      inputs = split_batch_input(input_str) if Settings.enable_batch else [input_str]
      for raw in inputs:
         await self._send_one(session, raw.strip())

   async def _send_one(self, session: BaseSession, input_str: str):   
      if DialogManager.is_waiting_to_handle(session.id, input_str):
         return

      request = Request(input_str)
      if not request.cmd:
         return await session.err("Kein Befehl erkannt.")
      
      command = self._router.resolve(request.cmd, session.command_groups)
      if not command:
         return await session.err(f"Unbekannter Befehl: {request.cmd}")

      try:
         await self._domain.on_before_run_command(session, request, command)
         await command.run(session, request)
         await self._domain.on_after_run_command(session, request, command)

      except PermissionError as exc:
         LogService.permission(session, "command", command.key)
         await session.err(str(exc))

      except ValueError as exc:
         await session.err(str(exc))

      except Exception as exc:
         await session.err("Ein interner Fehler ist aufgetreten.")
         LogService.error(exc)