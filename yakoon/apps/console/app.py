
import asyncio
from yakoon.core.devtools import MemoryTrendMonitor
from yakoon.core.devtools import UnresolvedPromptMonitor
from yakoon.engine import Engine, Output, safe_input
from yakoon.engine.settings import DEV_MODE
from yakoon.solution.registry import SolutionRegistry
from yakoon.solution.settings import SolutionSettings
from yakoon.services.renderer import RenderMode

# Set the global rendering mode to ansi text (no Markdown formatting)
SolutionSettings.runtime.render_mode = RenderMode.PLAIN

command_inits = ["welcome"]
#command_inits += ["batch: login stefan; switch; realm; ic stefan; version; switch;"]
command_inits += ["batch: login stefan; switch realm"]


async def run_console():
   
    if DEV_MODE:
        UnresolvedPromptMonitor.start()
        MemoryTrendMonitor.start(60)

    output = Output(print, print)
    
    engine = Engine(SolutionRegistry())
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