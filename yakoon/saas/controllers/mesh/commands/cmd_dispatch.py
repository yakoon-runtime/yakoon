import json
from yakoon.saas.commands.command import CmdNotFound
from yakoon.saas.commands.parser import Request
from yakoon.saas.controllers.mesh.commands.base import MeshCommand
from yakoon.saas.runtime.models.session import BaseSession


class CmdDispatch(MeshCommand):

    key = "*"

    async def run(self, session: BaseSession, request: Request):

        proxies = self.controller.get_proxy_controllers(session.tenant)        
        for controller in proxies.controllers.values():
            command = controller.commands.get(request.cmd)
            if command:
                return await controller.websocket.send_text(
                    json.dumps(command.__dict__))
        
        raise CmdNotFound(f"{request.cmd}")
