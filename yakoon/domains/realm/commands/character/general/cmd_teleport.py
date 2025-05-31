
from yakoon.core.command import Command
from yakoon.core.parser import Request
from yakoon.domains.platform.runtime.session import PlatformSession


class CmdTeleport(Command):

    key = "teleport"
    aliases = ["tel", "tp"]
    requires = ["admin"]
    requires_character = True

    async def run(self, session: PlatformSession, request: Request):

        await session.emit("teleport done!")
