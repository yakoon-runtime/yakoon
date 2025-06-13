
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


    print(registration_payload)

    await ws.send(json.dumps(registration_payload))