from yakoon.base.commands.command import MeshCommand
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session import BaseSession


class CmdWelcome(MeshCommand):

    key = "welcome"    
    template_key = "gateway/system/cmd_welcome"

    requires = ["system"]

    async def run(self, session: BaseSession, _: Request):

        presenter = await self.get_presenter(session)
        await presenter.emit("show")