import json

from fastapi import APIRouter, WebSocket
from fastapi import WebSocket, WebSocketDisconnect
from yakoon.mesh.controllers.base.base import BaseController
from yakoon.saas.controllers.base.base import SaasBaseController
from yakoon.saas.controllers.mesh.commands.cmdset import MeshCommandSet
from yakoon.mesh.models.tenent import CommandProxy, ControllerProxy, Tenent
from yakoon.mesh.runtime.session import BaseSession


ws_router = APIRouter()
@ws_router.websocket("/ws/loop")
async def loop_ws(websocket: WebSocket):
    await MeshController.instance().handle_loop_connection(websocket)


class MeshController(SaasBaseController):

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
        self.tenants: dict[str, Tenent] = {}
        MeshController._instance = self

    def get_proxy_controllers(self, tenant_id: str):
        return self.tenants.setdefault(tenant_id, Tenent(tenant_id))

    def register(self, tenant_id: str, controller_id: str, commands: list[dict], websocket):
        tenant = self.tenants.setdefault(tenant_id, Tenent(tenant_id))

        command_map = {}
        for cmd in commands:
            key = cmd["key"]
            if key in command_map:
                raise ValueError(f"Duplicate command key in controller '{controller_id}': {key}")
            command_map[key] = CommandProxy(cmd["key"], "", "") #TODO: add the other values.

        proxy = ControllerProxy(
            id=controller_id,
            commands=command_map,
            websocket=websocket,
        )

        tenant.controllers[controller_id] = proxy
    

    def unregister(self, websocket):
        for tenant in self.tenents.values():
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
                    controllers = msg["controllers"]
                    for controller in controllers:
                        self.register(
                            tenant_id=msg["tenant"],
                            controller_id=controller["controller_id"],
                            commands=controller["commands"],
                            websocket=websocket,
                        )
                    data = json.dumps({"type": "registered"})
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

        except WebSocketDisconnect as e:
            print(e)
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
