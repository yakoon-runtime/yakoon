from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session import Session
from yakoon.base import ports


class CmdCustomerValidate(Command):

    key = "wf:crm.customer.validate"

    async def run(self, session: Session, request: Request):

        wf = self.services.get(ports.WorkflowService)

        batch_id = self.context.batch_id
        batch = wf.runtime(session).get(batch_id)
        step_id = batch.current_step

        mail = batch.values.get("customer.mail")
        mail_opt_in = batch.values.get("customer.mail_opt_in")

        state = "unknown"

        if mail_opt_in in {"yes", "true", "1"}:
            if mail and mail.endswith("@enterprise.com"):
                state = "save"

        wf.set_value(session, batch_id, "validate.state", state)
