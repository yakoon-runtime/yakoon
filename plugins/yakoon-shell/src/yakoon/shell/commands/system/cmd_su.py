from yakoon.base.commands.command import BatchCommand
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session import Session


class CmdSu(BatchCommand):

    key = "su"    
    template_prefix = "system"

    batch_commmands = "use auth; {raw}; exit;"

    requires = ["system"]

    async def run(self, session: Session, request: Request):
       
        command = self.batch_commmands.format(raw=request.raw)
        await super().run(session, Request(command))