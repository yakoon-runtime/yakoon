  

from typing import Type
from yakoon.base.commands.command import Command, CommandKind, CommandVisibility
from yakoon.base.commands.request import Request
from yakoon.base.ports import WorkflowService
from yakoon.base.runtime.session.session import Session


def CmdWfStart(command_key: str, tem_prefix: str="", *, workflow_key: str | None = None) -> Type[Command]:
    """
    Generates a Command class that starts a workflow.

    - command_key: CLI key (e.g. "create-customer")
    - workflow_key: workflow file key; defaults to command_key
    """
    wf_key = workflow_key or command_key

    class _CmdWorkflowStart(Command):

        key = command_key
        template_prefix = tem_prefix
        kind = CommandKind.WORKFLOW
        visibility = CommandVisibility.NORMAL

        async def run(self, session: Session, request: Request):
            wf = self.services.get(WorkflowService)
            controller_id = self.context.controller.id

            batch_id = wf.start(
                session,
                controller_id,
                workflow_key=wf_key,
                enqueue_first=False,
            )
            wf.enqueue_next(session, batch_id)

    _CmdWorkflowStart.__name__ = f"CmdWfStart_{
        command_key.replace('-', '_'), 
        tem_prefix}"
    
    return _CmdWorkflowStart


