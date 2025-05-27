
import asyncio
from aioconsole import ainput
from yakoon.engine.core.io import IOAdapter
from yakoon.engine.runtime import Engine
from yakoon.platform.render.resolver import RenderMode
from yakoon.solution.platform.registry import SolutionRegistry
from yakoon.solution.settings import SolutionSettings


# Set the global rendering mode to ansi text (no Markdown formatting)
SolutionSettings.runtime.render_mode = RenderMode.PLAIN

command_inits = []
#command_inits += ["batch: login stefan; switch; mud; ic stefan; version; switch;"]
command_inits += ["batch: login stefan; switch mud; ic stefan;"]

async def run_console():
   
    io = IOAdapter(print, print)
    engine = Engine(SolutionRegistry())
    await engine.signal_ready(io)
    
    while True:               
        await asyncio.sleep(0.1)

        command = (command_inits.pop(0).strip() 
           if command_inits else await ainput("Command:> "))
        
        await engine.send("cli", command, io)
        
if __name__ == "__main__":
    asyncio.run(run_console())