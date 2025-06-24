import json
from yakoon.mesh.commands.command import CmdNotFound
from yakoon.mesh.commands.parser import Request
from yakoon.saas.controllers.mesh.commands.base import MeshCommand
from yakoon.mesh.runtime.session import BaseSession


class CmdDispatch(MeshCommand):

    key = "*"

    async def run(self, session: BaseSession, request: Request):
        
        """
        trace_id
        PendingResponseRegistry.register(
            trace_id=trace_id,
            session=session,
            request=request,
            command=command,
            controller=controller
        )
        """

        proxies = self.controller.get_proxy_controllers(session.tenant)        
        for controller in proxies.controllers.values():
            command = controller.commands.get(request.cmd)
            if command:
                msg = {
                    "type": "dispatch_command", 
                    "controller_id": controller.id, 
                    "cmd_key": command.key,
                    "raw": request.raw,
                    "kwargs": request.kwargs,
                    "session": session.to_row()
                }
                return await controller.websocket.send_text(json.dumps(msg))
        
        raise CmdNotFound(f"{request.cmd}")
