from yakoon.base import ports
from yakoon.base.commands.command import WfCommand
from yakoon.base.commands.request import Request
from yakoon.base.models.command import CommandVisibility
from yakoon.base.models.fields import FormSpec
from yakoon.base.models.mode import InteractionMode
from yakoon.base.runtime.session.session import Session


class CmdWfInput(WfCommand):

    key = "wf.input"
    visibility = CommandVisibility.INTERNAL

    async def run(self, session: Session, request: Request) -> None:  # noqa: ARG002
        batch_id = request.arg(0)
        step_id = request.arg(1)

        wfsvc = self.services.get(ports.WorkflowService)
        policies = self.services.get(ports.PolicyService)
        inputs = self.services.get(ports.InputService)

        step = wfsvc.get_step(session, batch_id=batch_id, step_id=step_id)
        s = step.input

        # 1) build fieldspecs
        fields = []
        for f in s.fields:
            base = policies.get_field(f.policy or "system:string")
            # options/default are step-specific overrides
            field = base.fork(
                key=f.var,
                label=f.title or base.label,
                required=f.required,
                options=f.options or None,
                default=f.default,
            )
            fields.append(field)

        # 2) collect values depending on mode
        values: dict[str, object]
        if session.interaction_mode == InteractionMode.FORM:
            spec = FormSpec(
                form_id=f"{batch_id}:{step_id}",
                batch_id=batch_id,
                step_key=step_id,
                title=s.title,
                fields=fields,
            )
            values = await inputs.ask_form(session, spec)
        else:
            values = {}
            for field in fields:
                values[field.key] = await inputs.ask_field(session, field)

        # complete input step
        wfsvc.complete_input_step(
            session,
            batch_id=batch_id,
            step_id=step_id,
            values=values,
        )
