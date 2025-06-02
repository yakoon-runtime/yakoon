from yakoon.commands.parser import Request
from yakoon.domains.gateway.commands.base import PlatformCommand
from yakoon.domains.gateway.runtime.session import GatewaySession


class CmdWelcome(PlatformCommand):

    key = "welcome"    
    template_key = "system/cmd_welcome"

    requires = ["system"]

    async def run(self, session: GatewaySession, _: Request):

        presenter = await self.get_presenter(session)
        await presenter.emit("show")