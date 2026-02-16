from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.ports import WorkflowService
from yakoon.base.runtime.session.session import Session


def CmdWfStart(command_key: str) -> type[Command]:
    """
    Generates a Command class that starts a workflow.

    - command_key: CLI key (e.g. "create-customer")
    - alt_command_key: workflow file key; defaults to command_key
    """

    class _CmdWorkflowStart(Command):

        key = command_key
        template_prefix = None

        async def run(self, session: Session, request: Request) -> None:  # noqa: ARG002
            wf = self.services.get(WorkflowService)
            controller_id = self.context.controller.id

            batch_id = wf.start(
                session,
                controller_id,
                command_key=_CmdWorkflowStart.key,
                enqueue_first=False,
            )
            wf.enqueue_next(session, batch_id)

    _CmdWorkflowStart.__name__ = f"CmdWfStart_{
        command_key.replace('-', '_')}"

    return _CmdWorkflowStart
