
from engine.core.command import Command
from engine.core.parser import Request
from engine.runtime.session import Session


class CmdLook(Command):

    key = "look"
    aliases = ["see"]

    async def run(self, session: Session, request: Request):
        char = session.character
        room = session.ctx.game.room_store.get(char.location) if char else None
        if not room:
            return await session.err("Du bist nirgendwo.")

        await session.out(room.render(session))