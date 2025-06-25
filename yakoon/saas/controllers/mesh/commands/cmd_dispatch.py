import asyncio
import json
import uuid
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

        trace_id = uuid.uuid4().hex
        fut = asyncio.get_running_loop().create_future()
        self.controller.pending[trace_id] = (session, fut)

        proxies = self.controller.get_proxy_controllers(session.tenant)        
        for controller in proxies.controllers.values():
            command = controller.commands.get(request.cmd)
            if command:
                msg = {
                    "type": "dispatch_command", 
                    "trace_id": trace_id,
                    "controller_id": controller.id, 
                    "cmd_key": command.key,
                    "raw": request.raw,
                    "kwargs": request.kwargs,
                    "session": session.to_row()
                }
                await controller.websocket.send_text(json.dumps(msg))
                await fut # block here
                return
                        
        raise CmdNotFound(f"{request.cmd}")
