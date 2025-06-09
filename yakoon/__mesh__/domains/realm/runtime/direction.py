from yakoon.saas.domains.realm.behavior import CharacterBehavior
from yakoon.saas.commands.command import Command
from yakoon.saas.commands.commandset import CommandSet
from yakoon.saas.commands.parser import Request
from yakoon.saas.runtime.models.session import BaseSession


class DirectionCommand(Command):

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


def get_exit_direction_commandset(room) -> list[Command]:
    exits = getattr(room, "exits", {})
    return CommandSet.build_command_set([
        DirectionCommand(key=dir, target=room_id)
        for dir, room_id in exits.items()])