from uuid import uuid4
from yakoon.base import ports
from yakoon.base.ports import AuditLogService
from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session import Session


class CmdCreateCustomer(Command):

    key = "crm.customer.create"

    async def run(self, session: Session, request: Request):

        audits = self.services.get(AuditLogService)
        presenter = await self.get_presenter(session)

        first = request.option("first")
        last = request.option("last")
        if not first or not last:
            raise ValueError("Missing required parameters: --first, --last")

        customer_id = f"CUST-{uuid4().hex[:8]}"

        await audits.audit(f"Create Customer: {first} {last} (id={customer_id})")
        await presenter.emit("created")

        wf = self.services.get(ports.WorkflowService)
        wf.set_value(session, request.batch_id, "customer.id", customer_id)
