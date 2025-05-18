from engine.core.command import Command
from engine.core.commandset import CommandSet
from engine.core.parser import Request
from engine.runtime.session import Session


class DirectionCommand(Command):

    key = "" # key is set by runtime
    aliases = [] # alias is set by runtime

    def __init__(self, key: str, target: str):
        self.key = key
        self.aliases = []
        self._target = target

    async def run(self, session: Session, request: Request):
        char = session.character
        char.location = self._target

        room = session.ctx.game.room_store.get(self._target)
        session.ctx.game.update_room_commands(session, room)

        await session.out(f"Du gehst nach |w{room.name}|n.")
        await session.out(room.render(session))

    
def get_exit_direction_commandset(room) -> CommandSet:
    exits = getattr(room, "exits", {})
    return CommandSet.build_command_set([
        DirectionCommand(key=dir, target=room_id)
        for dir, room_id in exits.items()])