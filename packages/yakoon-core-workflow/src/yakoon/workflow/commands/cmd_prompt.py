from yakoon.base import ports
from yakoon.base.commands.command import CommandVisibility, WfCommand
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session import Session


class CmdWfPrompt(WfCommand):

    key = "wf.prompt"
    visibility = CommandVisibility.INTERNAL

    async def run(self, session: Session, request: Request) -> None:  # noqa: ARG002

        batch_id = request.arg(0)
        step_id = request.arg(1)

        wfsvc = self.services.get(ports.WorkflowService)
        policies = self.services.get(ports.PolicyService)
        inputs = self.services.get(ports.InputService)

        step = wfsvc.get_step(session, batch_id, step_id)
        p = step.prompt

        base = policies.get_field(p.policy or "system:string")
        field = base.fork(key=p.var, label=p.title)

        # TEXT
        if p.kind == "text":
            value = await inputs.ask_field(session, field)
            wfsvc.complete_prompt_step(
                session, batch_id=batch_id, step_id=step_id, value=value
            )
            return

        # SELECT (returns option.value)
        if p.kind == "select":
            value = await inputs.choice_value(
                session,
                field,
                p.options,
                default=p.default,  # falls du default schon nutzen willst
            )
            wfsvc.complete_prompt_step(
                session, batch_id=batch_id, step_id=step_id, value=value
            )
            return

        # CONFIRM (returns bool)
        if p.kind == "confirm":
            value = await inputs.confirm(session, field)
            wfsvc.complete_prompt_step(
                session, batch_id=batch_id, step_id=step_id, value=value
            )
            return

        raise RuntimeError(f"Unsupported prompt kind: {p.kind!r}")
