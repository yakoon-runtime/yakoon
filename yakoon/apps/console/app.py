
import asyncio
from aioconsole import ainput
from yakoon.engine.runtime import Engine
from yakoon.platform.render.render_mode import RenderMode
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

    asyncio.create_task(engine.send(session_id, "batch: login stefan; switch mud; help", msg, err))
    while True:
        command = await ainput("|:> ")
        asyncio.create_task(engine.send(session_id, command, msg, err))

if __name__ == "__main__":
    asyncio.run(run_console())