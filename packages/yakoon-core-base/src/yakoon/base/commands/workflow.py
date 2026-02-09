

from yakoon.base import ports
from yakoon.base.commands.command import Command
from yakoon.base.models.workflow import WorkflowRuntime
from yakoon.base.runtime.session.session import Session


class WfCommand(Command):
    """
    A command that schedules follow-up commands into the CommandQueueService.
    It does not execute them itself.
    """

    def _workflow_runtime(self, session: Session) -> WorkflowRuntime:
        meta = session._runtime.meta
        if "workflow" not in meta:
            meta["workflow"] = WorkflowRuntime()
        return meta["workflow"]

    def schedule(self, session: Session, commands: list[str]) -> str:
        queue = self.services.get(ports.CommandQueueService)
        bid = queue.enqueue_commands(session, commands)

        wf = self._workflow_runtime(session)
        wf.ensure(bid, interaction_mode=session.interaction_mode)
        
        return bid
    

