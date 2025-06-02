from yakoon.domains.realm.behavior import CharacterBehavior
from yakoon.domains.realm.runtime.data import RuntimeRealmData
from yakoon.commands.command import Command
from yakoon.commands.commandset import CommandSet
from yakoon.commands.parser import Request
from yakoon.domains.gateway.runtime.session import PlatformSession


class DirectionCommand(Command):

    key = "" # key is set by runtime
    aliases = [] # alias is set by runtime

    def __init__(self, key: str, target: str):
        self.key = key
        self.aliases = []
        self._target = target

    async def get_template_path(self):
        return await super().get_template_path()

    async def run(self, session: PlatformSession, request: Request):
        runtime_data: RuntimeRealmData = session.data_runtime
        character = runtime_data.character

        CharacterBehavior.attach(character)
        await character.move_to(session, self._target)


def get_exit_direction_commandset(room) -> list[Command]:
    exits = getattr(room, "exits", {})
    return CommandSet.build_command_set([
        DirectionCommand(key=dir, target=room_id)
        for dir, room_id in exits.items()])