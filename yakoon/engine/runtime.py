
from yakoon.engine.core.dialog.manager import DialogManager
from yakoon.engine.core.game.definition import BaseGameDefinition
from yakoon.engine.core.parser import Request, request_to_debug_dict
from yakoon.engine.core.router import CommandRouter
from yakoon.engine.services.log_service import LogService
from yakoon.engine.system.session import (
   BaseSession, OnGetSession, PrintError, PrintMessage, Sessions)


class Engine():
     
   def __init__(self):
      """
      Creates a new instance of the class engine.
      """
      self._game: BaseGameDefinition = None
      self._sessions = Sessions(self)
      self._router = CommandRouter()

   @property
   def router(self) -> CommandRouter:
        return self._router

   async def enter(self, session_id: str,
                   on_print_msg: PrintMessage,
                   on_print_err: PrintError,
                   on_get_session: OnGetSession):      

      async def _on_create_new(session: BaseSession):
         session.out = on_print_msg
         session.err = on_print_err
         session.command_groups = self._game.default_command_groups or []
         await on_get_session(session)
 
      await self._sessions.create_session(session_id, _on_create_new, on_get_session)

   async def listen(self, session: BaseSession, input_str: str):   
      if DialogManager.is_waiting_to_handle(session.id, input_str):
         return

      request = Request(input_str)
      if not request.cmd:
         return await session.err("Kein Befehl erkannt.")
      await session.out(request_to_debug_dict(request))

      command = self._router.resolve(request.cmd, session.command_groups)
      if not command:
         return await session.err(f"Unbekannter Befehl: {request.cmd}")

      try:
         await self._game.on_before_run_command(session, request, command)
         await command.run(session, request)
         await self._game.on_after_run_command(session, request, command)

      except PermissionError as exc:
         LogService.permission(session, "command", command.key)
         await session.err(str(exc))

      except ValueError as exc:
         await session.err(str(exc))

      except Exception as exc:
         await session.err("Ein interner Fehler ist aufgetreten.")
         LogService.error(exc)
                  
   def load_game(self, game: BaseGameDefinition):
      self._game = game
      for commands_set in game.commandsets:
         mode = getattr(commands_set, "mode", "system")
         self._router.register(mode, commands_set)
