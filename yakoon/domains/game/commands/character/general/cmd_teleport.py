
from yakoon.engine.core.command import Command
from yakoon.engine.core.parser import Request
from yakoon.solution.platform.runtime.session import SolutionSession


class CmdTeleport(Command):

    key = "teleport"
    aliases = ["tel", "tp"]
    requires = ["admin"]
    requires_character = True

    async def run(self, session: SolutionSession, request: Request):

        await session.emit("teleport done!")
