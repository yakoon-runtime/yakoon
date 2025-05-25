from yakoon.engine.core.command import Command
from yakoon.engine.core.parser import Request
from yakoon.solution.platform.runtime.session import SolutionSession


class CmdOOC(Command):

    key = "ooc"

    async def run(self, session: SolutionSession, request: Request):
        if not session.character:
            return await session.err("Du bist bereits OOC.")

        name = session.character.name
        session.character = None
        #session.cmd_groups = ["account"]
        await session.out(f"Du bist nun OOC. Charakter '{name}' wurde verlassen.")