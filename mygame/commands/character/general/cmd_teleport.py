
from engine.core.command import Command
from engine.core.parser import Request
from mygame.runtime.session import GameSession


class CmdTeleport(Command):

    key = "teleport"
    aliases = ["tel", "tp"]
    requires = ["admin"]

    async def run(self, session: GameSession, request: Request):

        await session.out("teleport done!")
