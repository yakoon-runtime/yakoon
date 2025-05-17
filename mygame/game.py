
from engine.core.game.definition import BaseGameDefinition
from mygame.commands.general.cmdset import GeneralCommands
from mygame.stores.room_store import RoomStore

class GameDefinition(BaseGameDefinition):

    commandsets = [GeneralCommands]
    room_store = RoomStore
    # optional: template_renderer, ask_handler, etc.
