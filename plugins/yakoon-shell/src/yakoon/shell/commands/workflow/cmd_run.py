from yakoon.base import ports
from yakoon.base.commands.workflow import WfCommand
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session.session import Session


class CmdWfRun(WfCommand):

    key = "wf.run"

    async def run(self, session: Session, request: Request):
        key = request.arg(0)                  # "kunden_anlage" oder "shell:kunden_anlage"
        controller_id = self.controller.id    # kommt aus deinem Dispatcher

        wfsvc = self.services.get(ports.WorkflowService)        
        wfsvc.start(session, controller_id, key, interaction_mode=session.interaction_mode)