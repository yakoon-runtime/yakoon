
from engine.core.command import Command
from engine.core.parser import Request
from mygame.runtime.session import GameSession
from mygame.stores.room_store import RoomStore

class CmdLook(Command):

    key = "look"
    aliases = ["see"]

    async def run(self, session: GameSession, request: Request):
        char = session.character
        room = RoomStore.get(char.location) if char else None
        if not room:
            return await session.err("Du bist nirgendwo.")

        await session.out(await room.render(session))