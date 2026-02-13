from yakoon.base.commands.request import Request
from yakoon.base.commands.command import Command
from yakoon.base.ports import WorkflowService
from yakoon.base.runtime.session import Session


class CmdSu(Command):

    key = "su"

    template_prefix = "system"

    async def run(self, session: Session, request: Request):
        wf = self.services.get(WorkflowService)

        controller_id = self.context.controller.id
        batch_id = wf.start(session, controller_id, 
                            workflow_key=self.key, enqueue_first=False)

        wf.set_value(session, batch_id, "user.name", request.arg(0))
        wf.set_value(session, batch_id, "user.password", request.arg(1))

        wf.enqueue_next(session, batch_id)
