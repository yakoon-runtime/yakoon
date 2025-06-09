
import uvicorn
import asyncio
from fastapi import FastAPI

from yakoon.saas.engines.render.models.mode import RenderMode
from yakoon.saas.models.key import Key
from yakoon.saas.runtime.devtools import MemoryTrendMonitor
from yakoon.saas.runtime.devtools import UnresolvedPromptMonitor
from yakoon.saas.engines.command import Engine, Output, safe_input
from yakoon.saas.engines.command.settings import DEV_MODE
from yakoon.saas.bootstrap.registry import BootstrapControllerDirectory
from yakoon.saas.bootstrap.settings import SolutionSettings


# Set the global rendering mode to ansi text (no Markdown formatting)
SolutionSettings.runtime.render_mode = RenderMode.PLAIN

command_inits = ["welcome"]
#command_inits += ["batch: login stefan; switch; realm; ic stefan; version; switch;"]
#command_inits += ["batch: login Stefan; switch realm; ic Stefan"]
#command_inits += ["batch: login Stefan; switch mesh"]
command_inits += ["ping"]

async def run_console():
   
    if DEV_MODE:
        UnresolvedPromptMonitor.start()
        MemoryTrendMonitor.start(20)

    # FastAPI App vorbereiten
    app = FastAPI()
    from yakoon.saas.controllers.mesh.controller import ws_router
    app.include_router(ws_router)

    # Starte FastAPI-Server als Hintergrundtask
    async def start_api():
        config = uvicorn.Config(app=app, host="127.0.0.1", port=8000, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()

    # Starte API nebenläufig
    asyncio.create_task(start_api())

    output = Output(print, print)
    engine = Engine(BootstrapControllerDirectory())

    await engine.initialize(output)
    session = Key.from_parts("yakoon", "bucket", "develop", "cli")

    while True:                       
        command = (command_inits.pop(0).strip() 
           if command_inits else await safe_input())
        await engine.dispatch(session, command, output)


if __name__ == "__main__":    
   asyncio.run(run_console())

   if DEV_MODE: 
        UnresolvedPromptMonitor.stop() 
        MemoryTrendMonitor.stop()