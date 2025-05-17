
from engine.app import Engine
from engine.core.game.definition import BaseGameDefinition
from engine.runtime.session import Session
from mygame.commands.account.general.cmdset import GeneralAccountCommands
from mygame.commands.character.general.cmdset import GeneralCharacterCommands
from mygame.protocols.character_store import CharacterStoreProtocol
from mygame.protocols.object_store import ObjectStoreProtocol
from mygame.protocols.room_store import RoomStoreProtocol
from mygame.runtime.direction import get_exit_direction_commands
from mygame.stores.character_store import CharacterStore
from mygame.stores.object_store import ObjectStore
from mygame.stores.room_store import RoomStore


class GameDefinition(BaseGameDefinition):

    commandsets = [GeneralAccountCommands, GeneralCharacterCommands] 
    room_store: RoomStoreProtocol = RoomStore
    character_store: CharacterStoreProtocol = CharacterStore
    object_store: ObjectStoreProtocol = ObjectStore

    # optional: template_renderer, ask_handler, etc.

    @classmethod
    def update_room_commands(cls, session:Session, room=None):
        char = session.character
        if char:
            room = cls.room_store.get(char.location)
        router = session.ctx.router
        router.remove_dynamic_commands_for_session(session)
        for cmd in get_exit_direction_commands(room):
                router.register_dynamic_commands(cmd, session=session)         