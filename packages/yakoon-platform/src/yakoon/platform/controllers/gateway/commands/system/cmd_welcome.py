from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session import Session


class CmdWelcome(Command):

    key = "welcome"    
    template_key = "gateway/system/cmd_welcome"

    requires = ["system"]

    async def run(self, session: Session, _: Request):

        presenter = await self.get_presenter(session)
        await presenter.emit("show")