import json
from typing import Optional

from fastapi import WebSocket, WebSocketDisconnect
from fastapi import APIRouter, WebSocket
from fastapi import WebSocket, WebSocketDisconnect
from yakoon.saas.controllers.base.base import BaseController
from yakoon.saas.controllers.mesh.commands.cmdset import MeshCommandSet
from yakoon.saas.runtime.mesh.tanent import CommandProxy, ControllerProxy, Tanent
from yakoon.saas.runtime.models.session import BaseSession


ws_router = APIRouter()
@ws_router.websocket("/ws/loop")
async def loop_ws(websocket: WebSocket):
    await MeshController.instance().handle_loop_connection(websocket)


class MeshController(BaseController):

    id: str = "mesh"
    """Unique identifier used for command prefix resolution (e.g. realm:look, system:help)."""

    default_command_groups = ["system", "account"]     
    """Names of command groups that are automatically active for every session, 
    without requiring explicit permissions."""

    commandsets = [
        MeshCommandSet, 
        ]
    """ The collection of all commands. """

    @staticmethod
    def instance():
        return MeshController._instance

    def __init__(self):
        super().__init__()
        self.tanents: dict[str, Tanent] = {}
        MeshController._instance = self

    def get_proxy_controllers(self, tenant_id: str):
        return self.tanents.setdefault(tenant_id, Tanent(tenant_id))

    def register(self, tenant_id: str, controller_id: str, commands: list[dict], websocket):
        tenant = self.tanents.setdefault(tenant_id, Tanent(tenant_id))
        proxy = ControllerProxy(
            controller_id=controller_id,
            commands={cmd["name"]: CommandProxy(**cmd) for cmd in commands},
            websocket=websocket,
        )
        tenant.controllers[controller_id] = proxy        

    def unregister(self, websocket):
        for tenant in self.tanents.values():
            for ctrl_id, proxy in list(tenant.controllers.items()):
                if proxy.websocket == websocket:
                    del tenant.controllers[ctrl_id]     
    
    async def handle_loop_connection(self, websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                raw = await websocket.receive_text()
                msg = json.loads(raw)

                if msg.get("type") == "register_controller":
                    self.register(
                        tenant_id=msg["tenant"],
                        controller_id=msg["controller_id"],
                        commands=msg["commands"],
                        websocket=websocket,
                    )
                    data = json.dumps("registered")
                    await websocket.send_text(data)

                #elif msg.get("type") == "command":
                #    request = CommandRequest(**msg["payload"])
                #    response = await self.command_mesh.dispatch(request)
                #    await websocket.send_text(json.dumps(response.__dict__))

                """
                case "command":
                    req = CommandRequest(**msg["payload"])
                    controller = command_mesh.resolve(req.tenant, req.controller)
                    response = await controller.dispatch(req)
                    await websocket.send_text(json.dumps(response.__dict__))

                case "ping":
                    await websocket.send_text(json.dumps({"pong": True}))
                """

        except WebSocketDisconnect:
            self.unregister(websocket)
        
    async def on_initialize(self, session: BaseSession):
        """
        Called after the controller has been fully constructed but before any commands are processed.

        Use this hook to perform asynchronous setup tasks such as loading data, initializing services,
        or validating infrastructure state (e.g., ensuring the admin account exists).

        This method is guaranteed to run once before the first engine tick or command dispatch.
        """
        pass
            
    async def on_before_run_command(self, session: BaseSession, request, command):
        """
        Hook called immediately before a single command is executed.
        Can be used to enforce permissions, inject context, or audit.
        """
        pass
