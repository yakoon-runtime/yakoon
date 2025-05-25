
from yakoon.engine.core.command import Command
from yakoon.engine.core.parser import Request
from yakoon.solution.platform.runtime.session import SolutionSession


class CmdTeleport(Command):

    key = "teleport"
    aliases = ["tel", "tp"]
    requires = ["admin"]

    async def run(self, session: SolutionSession, request: Request):

        await session.out("teleport done!")
