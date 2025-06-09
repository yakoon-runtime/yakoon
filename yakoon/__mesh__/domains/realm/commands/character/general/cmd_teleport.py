
from yakoon.saas.commands.parser import Request
from yakoon.saas.domains.realm.commands.base import RealmCommand
from yakoon.saas.runtime.models.session import BaseSession


class CmdTeleport(RealmCommand):

    key = "teleport"
    aliases = ["tel", "tp"]
    requires = ["admin"]
    template_key = "character/general/cmd_teleport"

    requires_character = True

    async def run(self, session: BaseSession, request: Request):

        await session.emit("teleport done!")
