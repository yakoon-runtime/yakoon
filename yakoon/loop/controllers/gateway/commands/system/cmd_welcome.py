from yakoon.loop.controllers.gateway.commands.base import LoopCommand
from yakoon.loop.runtime.commands.parser import Request
from yakoon.loop.runtime.runtime.session.session import BaseSession


class CmdWelcome(LoopCommand):

    key = "welcome"    
    template_key = "system/cmd_welcome"

    requires = ["system"]

    async def run(self, session: BaseSession, _: Request):

        presenter = await self.get_presenter(session)
        await presenter.emit("show")