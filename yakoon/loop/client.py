import asyncio
import json
import websockets

from yakoon.loop.config import LOOP_CONFIG
from yakoon.loop.controller import register_controller
from yakoon.loop.registry import CommandRegistry
from yakoon.loop.protocol import CommandRequest, CommandResponse

async def loop_main():
    
    uri = LOOP_CONFIG["url"]
    headers = {"Authorization": f"Bearer {LOOP_CONFIG['token']}"}

    # Register controller locally
    info = register_controller()

    async with websockets.connect(uri) as ws: #, extra_headers=headers) as ws:
        print("Connected to Yakoon MainLoop")

        # send registration
        await ws.send(json.dumps({
            "type": "register_controller",
            "tenant": LOOP_CONFIG["tenant"],
            "controller_id": info["controller_id"],
            "commands": info["commands"]
        }))

        # command loop
        while True:
            raw = await ws.recv()
            print(raw)            
            #data = json.loads(raw)
            await asyncio.sleep(0.1)
            continue

            if data.get("type") == "command":
                request = CommandRequest(**data["payload"])
                try:
                    result = CommandRegistry.dispatch(request.command, request.args)
                    response = CommandResponse(success=True, result=result)
                except Exception as e:
                    response = CommandResponse(success=False, result={}, error=str(e))
                await ws.send(json.dumps(response.__dict__))


if __name__ == "__main__":    
    asyncio.run(loop_main())