from yakoon.base import ports
from yakoon.base.commands.command import WfCommand, CommandVisibility
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session.session import Session


class CmdWfCancel(WfCommand):

    key = "wf.cancel"
    visibility = CommandVisibility.INTERNAL

    async def run(self, session: Session, request: Request):

        wfsvc = self.services.get(ports.WorkflowService)
        queue = self.services.get(ports.CommandQueueService)

        rt = wfsvc.runtime(session)

        batch_id = self.context.batch_id
        batch = rt.get(batch_id)
        if not batch:
            await session.notify("Kein aktiver Workflow.")
            return

        # 1) Queue abbrechen
        queue.cancel_batch(session, batch.batch_id)

        # 2) Runtime aufräumen
        rt.remove(batch.batch_id)

        # 3) Dialog ggf. schließen
        dialogs = self.services.get(ports.DialogService)
        if dialogs.is_waiting(session):
            dialogs.cancel_prompt(session)

        # 4) Feedback (optional)
        await session.write("Workflow abgebrochen.")
