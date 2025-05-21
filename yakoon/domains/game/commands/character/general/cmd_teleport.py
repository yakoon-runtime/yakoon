
from yakoon.engine.core.command import Command
from yakoon.engine.core.parser import Request
from yakoon.domains.game.runtime.session import GameSession


class CmdTeleport(Command):

    key = "teleport"
    aliases = ["tel", "tp"]
    requires = ["admin"]

    async def run(self, session: GameSession, request: Request):

        await session.out("teleport done!")
