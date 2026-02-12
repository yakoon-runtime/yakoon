from yakoon.base import ports
from yakoon.base.commands.command import Command, CommandKind, CommandVisibility
from yakoon.base.commands.request import Request
from yakoon.base.models.workflow import NotInWorkflowContext
from yakoon.base.runtime.session.session import Session


class CmdWfNext(Command):

    key = "wf.next"
    kind = CommandKind.WORKFLOW
    visibility = CommandVisibility.INTERNAL

    async def run(self, session: Session, request: Request):

        if not self.context.is_batch:
            raise NotInWorkflowContext()

        batch_id = request.arg(0)
        step_id  = request.arg(1)

        wfsvc = self.services.get(ports.WorkflowService)
        wfsvc.set_value(session, batch_id, "batch_id", batch_id)
        wfsvc.complete_run_step(session, batch_id=batch_id, step_id=step_id)
