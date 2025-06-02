
from yakoon.commands.command import Command
from yakoon.commands.parser import Request
from yakoon.domains.gateway.runtime.session import GatewaySession


class CmdTeleport(Command):

    key = "teleport"
    aliases = ["tel", "tp"]
    requires = ["admin"]
    requires_character = True

    async def run(self, session: GatewaySession, request: Request):

        await session.emit("teleport done!")
