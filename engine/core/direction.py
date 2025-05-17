

from engine.core.command import Command
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
        session.ctx.update_dynamic_commands(session, room)

        await session.out(f"Du gehst nach |w{room.name}|n.")
        await session.out(room.render())

    
def get_exit_direction_commands(room) -> list[Command]:
    exits = getattr(room, "exits", {})
    return [
        DirectionCommand(key=dir, target=room_id)
        for dir, room_id in exits.items()
    ]