
import json

import websockets
from yakoon.loop.commands.resolver import CommandResolver
from yakoon.loop.controllers.directory import AppControllerDirectory
from yakoon.loop.runtime.commands.parser import Request
from yakoon.loop.runtime.controllers.base.base import BaseController
from yakoon.loop.runtime.runtime.session.output import OutputWS
from yakoon.loop.settings import settings
from yakoon.mesh.runtime.session.session import BaseSession

async def start_loop(directory: AppControllerDirectory):
    
    resolver = CommandResolver(directory)

    registration_payload = {
        "type": "register_controller",
        "tenant": settings.loop.tenant,
        "controllers": resolver.collect_metadata()
    }

    async with websockets.connect(settings.loop.url) as ws: #, extra_headers=headers) as ws:
        print("Connected to Yakoon MainLoop")
        
        await ws.send(json.dumps(registration_payload))

        # Hold the connection open (wait for ping or message)
        while True:
            raw = await ws.recv()     # or sleep + heartbeat   
            if not raw:
                continue
            msg = json.loads(raw)         
            await handle_incoming_message(ws, msg, directory)


async def handle_incoming_message(ws, msg: dict, directory):
    match msg.get("type"):
        case "registered":
            print("✅ Registered")
        case "dispatch_command":
            await handle_run_command(ws, msg, directory)
        case _:
            print("⚠️ Unknown message type")


async def handle_run_command(ws, msg: dict, directory):
    try:
        session = None
        controller_id = msg.get("controller_id")
        cmd_key = msg.get("cmd_key")

        #trace_id = msg.get("trace_id", "-")

        request = Request(msg.get("raw"))
        controller: BaseController = directory.get(controller_id)
        gateway: BaseController = directory.gateway
        command = await controller.resolve_command(cmd_key)

        session_data = msg.get("session")
        session = BaseSession.from_row(session_data)
        session.bind_io(OutputWS(ws, msg["trace_id"]))
        
        await session.emit("Hello")

        await gateway.on_gateway_validate(session)
        await gateway.on_before_run_command(session, msg, command)

        await controller.on_before_run_command(session, request, command)
        #await command.run(session, request)
        await controller.on_after_run_command(session, request, command)

        await gateway.on_after_run_command(session, request, command)
        await gateway.on_gateway_finalize(session)

    except Exception as e:
        print(f"❌ Failed to handle command: {e}")
