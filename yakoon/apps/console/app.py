
import asyncio
from yakoon.engines.render.models.mode import RenderMode
from yakoon.runtime.devtools import MemoryTrendMonitor
from yakoon.runtime.devtools import UnresolvedPromptMonitor
from yakoon.engines.command import Engine, Output, safe_input
from yakoon.engines.command.settings import DEV_MODE
from yakoon.bootstrap.registry import BootstrapRegistry
from yakoon.bootstrap.settings import SolutionSettings


# Set the global rendering mode to ansi text (no Markdown formatting)
SolutionSettings.runtime.render_mode = RenderMode.PLAIN

command_inits = ["welcome"]
#command_inits += ["batch: login stefan; switch; realm; ic stefan; version; switch;"]
command_inits += ["batch: login stefan; switch realm"]


async def run_console():
   
    if DEV_MODE:
        UnresolvedPromptMonitor.start()
        MemoryTrendMonitor.start(20)

    output = Output(print, print)
    
    engine = Engine(BootstrapRegistry())
    await engine.initialize(output)

    while True:               
        
        command = (command_inits.pop(0).strip() 
           if command_inits else await safe_input())
                
        await engine.dispatch("cli", command, output)


if __name__ == "__main__":    
   asyncio.run(run_console())

   if DEV_MODE: 
        UnresolvedPromptMonitor.stop() 
        MemoryTrendMonitor.stop()