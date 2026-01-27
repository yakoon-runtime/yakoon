import json

from fastapi import APIRouter, WebSocket
from fastapi import WebSocket, WebSocketDisconnect
from yakoon.base.controllers.base.base import BaseController
from yakoon.platform.controllers.base.base import SaasBaseController
from yakoon.platform.controllers.mesh.commands.cmdset import MeshCommandSet
from yakoon.base.models.tenent import CommandProxy, ControllerProxy, Tenent
from yakoon.base.runtime.session import BaseSession


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

    pending: dict[str, tuple] = {}

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
                if not raw:
                    continue

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

                if msg.get("type") == "loop_msg":
                    trace_id = msg["trace_id"]
                    result = self.pending.pop(trace_id, None)
                    if result:
                        session, fut = result
                        if fut:
                            await session.emit(msg["text"])
                            fut.set_result(data)

                    #print(msg) # TODO: Hier müssen wir unsere Lifecycle wieder aufnehmen....
                    
                    #trace_id = msg["trace_id"]
                    #entry = PendingResponseRegistry.pop(trace_id)
                    #session = entry.session
                    #await session.emit(msg["text"])
                
 
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
