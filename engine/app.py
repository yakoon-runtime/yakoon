
from engine.core.dialog.manager import DialogManager
from engine.core.direction import get_exit_direction_commands
from engine.core.game.definition import BaseGameDefinition
from engine.core.parser import Request, request_to_debug_dict
from engine.core.router import CommandRouter
from engine.runtime.session import (
   Session, OnGetSession, PrintError, PrintMessage, Sessions)


class Engine():
     
   def __init__(self):
      """
      Creates a new instance of the class engine.
      """
      self._game: BaseGameDefinition = None
      self._sessions = Sessions(self)
      self._router = CommandRouter()

   async def enter(self, session_id: str,
                   on_print_msg: PrintMessage,
                   on_print_err: PrintError,
                   on_get_session: OnGetSession):      

      async def _on_result_session(session: Session):
         session.out = on_print_msg
         session.err = on_print_err
         await on_get_session(session)
 
      await self._sessions.create_session(session_id, _on_result_session)

   async def listen(self, session: Session, input_str: str):   
      if DialogManager.is_waiting_to_handle(session.id, input_str):
         return

      request = Request(input_str)
      if not request.cmd:
         return await session.err("Kein Befehl erkannt.")
      await session.out(request_to_debug_dict(request))

      command = self._router.resolve(request.cmd, session)
      if not command:
         return await session.err(f"Unbekannter Befehl: {request.cmd}")

      await command.run(session, request)

   def update_dynamic_commands(self, session: Session, room):
      char = session.character
      if char:
         room = self._game.room_store.get(char.location)
      self._router.remove_dynamic_commands_for_session(session)
      for cmd in get_exit_direction_commands(room):
            self._router.register(cmd, "dynamic", session=session)            
            
   def load_game(self, game: BaseGameDefinition):
      self._game = game
      for commands_set in game.commandsets:
         mode = getattr(commands_set, "mode", "system")
         for cmd_cls in commands_set.commands():
            self._router.register(cmd_cls, mode=mode)

