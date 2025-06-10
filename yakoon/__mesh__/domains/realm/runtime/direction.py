from yakoon.saas.domains.realm.behavior import CharacterBehavior
from yakoon.saas.commands.command import SaasCommand
from yakoon.mesh.commands.commandset import CommandSet
from yakoon.mesh.commands.parser import Request
from yakoon.mesh.runtime.session import BaseSession


class DirectionCommand(SaasCommand):

    key = "" # key is set by runtime
    aliases = [] # alias is set by runtime

    def __init__(self, key: str, target: str):
        self.key = key
        self.aliases = []
        self._target = target

    async def get_template_path(self):
        return await super().get_template_path()

    async def run(self, session: BaseSession, request: Request):
        character = session.ctx("realm", "char", persist=False)

        CharacterBehavior.attach(character)
        await character.move_to(session, self._target)


def get_exit_direction_commandset(room) -> list[SaasCommand]:
    exits = getattr(room, "exits", {})
    return CommandSet.build_command_set([
        DirectionCommand(key=dir, target=room_id)
        for dir, room_id in exits.items()])