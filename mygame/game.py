
from engine.core.commandset import CommandSet
from engine.core.game.definition import BaseGameDefinition
from engine.runtime.session import Session
from mygame.commands.account.general.cmdset import GeneralAccountCommands
from mygame.commands.account.login.cmdset import LoginAccountCommands
from mygame.commands.character.general.cmdset import GeneralCharacterCommands
from mygame.runtime.direction import get_exit_direction_commandset
from mygame.stores.session_store import SessionStore
from mygame.stores.account_store import AccountStore
from mygame.stores.character_store import CharacterStore
from mygame.stores.object_store import ObjectStore
from mygame.stores.room_store import RoomStore


class GameDefinition(BaseGameDefinition):

    default_command_groups = ["login"]     
    commandsets = [LoginAccountCommands, GeneralAccountCommands, GeneralCharacterCommands] 

    room_store = RoomStore
    character_store = CharacterStore
    object_store = ObjectStore
    account_store = AccountStore
    session_store = SessionStore

    # optional: template_renderer, ask_handler, etc.

    @classmethod
    def update_room_commands(cls, session:Session, room=None):
        char = session.character
        if char:
            room = cls.room_store.get(char.location)
        router = session.ctx.router
        router.unregister(session.id) # TODO: Check: oder room_id / Pro User eigene Engine?
        router.register(session.id, get_exit_direction_commandset(room))