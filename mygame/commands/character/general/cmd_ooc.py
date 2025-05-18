from engine.core.command import Command
from engine.core.parser import Request
from engine.runtime.session import Session
from mygame.runtime.character import leave_character_context


class CmdOOC(Command):

    key = "ooc"

    async def run(self, session: Session, request: Request):
        if not session.character:
            return await session.err("Du bist bereits OOC.")

        name = session.character.name
        session.command_groups = ["account"]
        leave_character_context(session)
        await session.out(f"Du bist nun OOC. Charakter '{name}' wurde verlassen.")