from yakoon.base.commands.request import Request
from yakoon.base.commands.workflow import WorkflowCommand
from yakoon.base.runtime.session import Session


class CmdSu(WorkflowCommand):

    key = "su"    
    template_prefix = "system"

    batch_commmands = "use auth; {raw}; exit;"

    async def run(self, session: Session, request: Request):

        #session.set_active_controller("auth")
        workflow = Request(request.raw).split_commands()
        self.schedule(session, workflow)



