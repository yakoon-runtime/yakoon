from uuid import uuid4
from yakoon.base import ports
from yakoon.base.ports import AuditLogService
from yakoon.base.commands.command import WfCommand
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session import Session


class CmdCustomerStore(WfCommand):

    key = "wf:crm.customer.store"


    async def run(self, session: Session, request: Request):

        audits = self.services.get(AuditLogService)
        wf = self.services.get(ports. WorkflowService)

        first = request.option("first")
        last = request.option("last")
        mail_opt_in = request.option("mail_opt_in")
        mail = request.option("mail")

        if not first or not last:
            raise ValueError("Missing required: --first, --last")

        # Optional: Konsistenz
        if mail_opt_in in {"yes", "true", "1"} and not mail:
            raise ValueError("mail_opt_in=yes requires --mail")

        customer_id = f"CUST-{uuid4().hex[:8]}"

        # “Ernte”: audit + event
        await audits.audit(f"Customer created: {first} {last} id={customer_id}")

        # TODO: Jetzt im Workflow weiter.... 

        # Ergebnis zurück in Workflow-Context
        #batch_id = request.arg(0)   # falls ihr batch_id/step_id als args übergebt
        #step_id  = request.arg(1)

        #wf.set_value(session, batch_id, "customer.id", customer_id)

        # Workflow weiterlaufen lassen
        #wf.complete_run_step(session, batch_id=batch_id, step_id=step_id)
