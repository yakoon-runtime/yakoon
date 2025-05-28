
import asyncio
from yakoon.engine.core.io.adapter import IOAdapter
from yakoon.engine.core.io.input import safe_input
from yakoon.engine.debug.memory import mem_monitor
from yakoon.engine.debug.zombie import detector
from yakoon.engine.runtime import Engine
from yakoon.engine.settings import DEV_MODE
from yakoon.platform.render.resolver import RenderMode
from yakoon.solution.platform.registry import SolutionRegistry
from yakoon.solution.settings import SolutionSettings


# Set the global rendering mode to ansi text (no Markdown formatting)
SolutionSettings.runtime.render_mode = RenderMode.PLAIN

command_inits = []
#command_inits += ["batch: login stefan; switch; realm; ic stefan; version; switch;"]
command_inits += ["batch: login stefan; switch realm; ic stefan;"]


async def run_console():
   
    if DEV_MODE:
        detector.start()
        mem_monitor.start()

    io = IOAdapter(print, print)

    engine = Engine(SolutionRegistry())
    await engine.signal_ready(io)

    while True:               
        
        command = (command_inits.pop(0).strip() 
           if command_inits else await safe_input())
                
        await engine.send("cli", command, io)


if __name__ == "__main__":    
   asyncio.run(run_console())

   if DEV_MODE: 
        detector.stop() 