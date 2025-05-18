from engine.core.command import Command
from engine.core.parser import Request
from engine.runtime.session import Session


class CmdOOC(Command):

    key = "ooc"

    async def run(self, session: Session, request: Request):
        if not session.character:
            return await session.err("Du bist bereits OOC.")

        name = session.character.name
        session.character = None
        session.ctx.game.update_room_commands(session)
        session.command_groups = ["account"]
        await session.out(f"Du bist nun OOC. Charakter '{name}' wurde verlassen.")