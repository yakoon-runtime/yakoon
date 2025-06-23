
import json

import websockets
from yakoon.loop.commands.resolver import CommandResolver
from yakoon.loop.controllers.directory import AppControllerDirectory
from yakoon.loop.settings import settings

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
            msg = json.loads(raw)         
            await handle_incoming_message(msg, directory)


async def handle_incoming_message(msg: dict, directory):
    match msg.get("type"):
        case "registered":
            print("✅ Registered")
        case "dispatch_command":
            await handle_run_command(msg, directory)
        case _:
            print("⚠️ Unknown message type")


async def handle_run_command(msg: dict, directory):
    try:
        session = None
        controller_id = msg.get("controller_id")
        cmd_key = msg.get("cmd_key")
        args = msg.get("args", {})

        #trace_id = msg.get("trace_id", "-")

        controller = directory.get(controller_id)
        command = await controller.resolve_command(cmd_key)

        #session = SessionFactory.create(tenant=settings.loop.tenant, trace_id=trace_id)

        await directory.gateway.on_gateway_validate(session)
        await controller.on_before_run_command(session, msg, command)
        await directory.gateway.on_before_run_command(session, msg, command)

        await command.run(session, args)

        await directory.gateway.on_gateway_finalize(session)

    except Exception as e:
        print(f"❌ Failed to handle command: {e}")
