from yakoon.commands.parser import Request
from yakoon.domains.gateway.commands.base import PlatformCommand
from yakoon.runtime.models.session import BaseSession


class CmdWelcome(PlatformCommand):

    key = "welcome"    
    template_key = "system/cmd_welcome"

    requires = ["system"]

    async def run(self, session: BaseSession, _: Request):

        presenter = await self.get_presenter(session)
        await presenter.emit("show")