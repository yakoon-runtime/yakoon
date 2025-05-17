

from engine.core.command import Command
from engine.core.parser import Request
from engine.runtime.session import Session

from mygame.stores.room_store import RoomStore

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

        room = RoomStore.get(self._target)
        await session.out(f"Du gehst nach |w{room.name}|n.")
        await session.out(room.render())

        await self._engine.update_dynamic_commands(session, room)

    
def get_exit_direction_commands(room) -> list[Command]:
    exits = getattr(room, "exits", {})
    return [
        DirectionCommand(key=dir, target=room_id)
        for dir, room_id in exits.items()
    ]