from engine.core.command import Command
from engine.core.commandset import CommandSet
from engine.core.parser import Request


class DirectionCommand(Command):

    key = "" # key is set by runtime
    aliases = [] # alias is set by runtime

    def __init__(self, key: str, target: str):
        self.key = key
        self.aliases = []
        self._target = target

    async def run(self, session, request: Request):
        await session.character.move_to(session, self._target)


def get_exit_direction_commandset(room) -> list[Command]:
    exits = getattr(room, "exits", {})
    return CommandSet.build_command_set([
        DirectionCommand(key=dir, target=room_id)
        for dir, room_id in exits.items()])