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
        session.ctx.update_dynamic_commands(session)
        await session.out(f"Du bist nun OOC. Charakter '{name}' wurde verlassen.")
