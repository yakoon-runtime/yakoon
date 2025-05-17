
from engine.core.command import Command
from engine.core.parser import Request
from engine.runtime.session import Session


class CmdTeleport(Command):

    key = "teleport"
    aliases = ["tel", "tp"]

    async def run(self, session: Session, request: Request):

        await session.out("teleport done!")
