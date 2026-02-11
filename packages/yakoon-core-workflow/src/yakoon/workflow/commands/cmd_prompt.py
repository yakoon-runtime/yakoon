from yakoon.base import ports
from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session.session import Session

from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session import Session
from yakoon.base import ports

from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session import Session
from yakoon.base import ports


class CmdWfPrompt(Command):

    key = "wf.prompt"
    
    async def run(self, session: Session, request: Request):
    
        batch_id = request.arg(0)
        step_id  = request.arg(1)

        prompts = self.services.get(ports.PromptService)
        wfsvc = self.services.get(ports.WorkflowService)
        
        step = wfsvc.get_step(session, batch_id, step_id)
        if not step.prompt:
            raise RuntimeError(f"Step '{step_id}' has no prompt")

        p = step.prompt

        # TEXT
        if p.kind == "text":
            value = await prompts.ask(session, p.title)
            wfsvc.complete_prompt_step(session, batch_id=batch_id, step_id=step_id, value=value)
            return

        # SELECT (returns option.value)
        if p.kind == "select":
            value = await prompts.choice_value(
                session,
                p.title,
                p.options,
                default=p.default,   # falls du default schon nutzen willst
            )
            wfsvc.complete_prompt_step(session, batch_id=batch_id, step_id=step_id, value=value)
            return

        # CONFIRM (returns bool)
        if p.kind == "confirm":
            value = await prompts.confirm(session, p.title)
            wfsvc.complete_prompt_step(session, batch_id=batch_id, step_id=step_id, value=value)
            return

        raise RuntimeError(f"Unsupported prompt kind: {p.kind!r}")
