from yakoon.commands.parser import Request
from yakoon.domains.gateway.commands.base import PlatformCommand
from yakoon.domains.gateway.runtime.session import PlatformSession


class CmdWelcome(PlatformCommand):

    key = "welcome"    
    template_key = "system/cmd_welcome"

    requires = ["system"]

    async def run(self, session: PlatformSession, _: Request):

        presenter = await self.get_presenter(session)
        await presenter.emit("show")