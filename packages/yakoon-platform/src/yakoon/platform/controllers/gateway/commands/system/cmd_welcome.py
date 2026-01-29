from yakoon.base.commands.request import Request
from yakoon.platform.controllers.gateway.commands.base import PlatformCommand
from yakoon.base.runtime.session import BaseSession


class CmdWelcome(PlatformCommand):

    key = "welcome"    
    template_key = "system/cmd_welcome"

    requires = ["system"]

    async def run(self, session: BaseSession, _: Request):

        presenter = await self.get_presenter(session)
        await presenter.emit("show")