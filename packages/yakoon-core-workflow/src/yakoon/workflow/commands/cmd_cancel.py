from yakoon.base import ports
from yakoon.base.commands.command import CommandVisibility, WfCommand
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session.session import Session
from yakoon.base.runtime.session.views import v_error


class CmdWfCancel(WfCommand):

    key = "wf.cancel"
    visibility = CommandVisibility.INTERNAL

    async def run(self, session: Session, request: Request) -> None:  # noqa: ARG002

        wfsvc = self.services.get(ports.WorkflowService)
        queue = self.services.get(ports.CommandQueueService)

        rt = wfsvc.runtime(session)

        batch_id = self.context.batch_id
        batch = rt.get(batch_id)
        if not batch:
            await session.emit(v_error("Kein aktiver Workflow."))
            return

        # 1) Queue abbrechen
        queue.cancel_batch(session, batch.batch_id)

        # 2) Runtime aufräumen
        rt.remove(batch.batch_id)

        # 3) Dialog ggf. schließen
        dialogs = self.services.get(ports.DialogService)
        if dialogs.is_waiting(session):
            dialogs.cancel_input(session)

        # 4) Feedback (optional)
        await session.write("Workflow abgebrochen.")
