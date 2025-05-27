
import asyncio
from aioconsole import ainput
from yakoon.engine.runtime import Engine
from yakoon.platform.render.resolver import RenderMode
from yakoon.solution.platform.registry import SolutionRegistry
from yakoon.solution.settings import SolutionSettings


# Set the global rendering mode to ansi text (no Markdown formatting)
SolutionSettings.runtime.render_mode = RenderMode.PLAIN


async def err(exc: Exception):
    print(exc)


async def msg(text: str):
    print(text)


async def run_console():
   
    session_id = "cli"
    engine = Engine(SolutionRegistry())
    await engine.signal_ready(msg)

    #command_inits = ["switch"]
    command_inits = ["batch: login stefan; switch; mud; ic stefan; version; switch;"]

    while True:               
        await asyncio.sleep(0.1)

        command = (command_inits.pop(0).strip() 
           if command_inits else await ainput("|:> "))
        
        await engine.send(session_id, command, msg, err)
        
if __name__ == "__main__":
    asyncio.run(run_console())