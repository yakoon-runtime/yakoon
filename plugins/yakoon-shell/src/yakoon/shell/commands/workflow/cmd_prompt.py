from yakoon.base import ports
from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session.session import Session

from yakoon.base.models.prompt import PromptMode


class CmdWfPrompt(Command):

    key = "wf.prompt"

    async def run(self, session: Session, request: Request):
        batch_id = request.arg(0)
        step_id  = request.arg(1)

        wfsvc = self.services.get(ports.WorkflowService)
        step = wfsvc.get_step(session, batch_id, step_id)

        await session.notify(step.prompt.title)

        dialogs = self.services.get(ports.DialogService)
        fut = dialogs.set_prompt(session, mode=PromptMode.NORMAL)
        value = await fut

        wfsvc.apply_prompt_value(
            session, batch_id=batch_id, step_id=step_id, value=value)


