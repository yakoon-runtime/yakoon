
from engine.core.game.definition import BaseGameDefinition
from mygame.commands.account.general.cmdset import GeneralAccountCommands
from mygame.commands.character.general.cmdset import GeneralCharacterCommands
from mygame.stores.character_store import CharacterStore
from mygame.stores.room_store import RoomStore


class GameDefinition(BaseGameDefinition):

    commandsets = [GeneralAccountCommands, GeneralCharacterCommands] 
    room_store = RoomStore
    character_store = CharacterStore

    # optional: template_renderer, ask_handler, etc.
