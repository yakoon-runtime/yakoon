
import asyncio
from aioconsole import ainput
from yakoon.engine.core.dialog.manager import DialogManager
from yakoon.engine.core.tools.output import OutputBufferManager
from yakoon.engine.runtime import Engine
from yakoon.platform.render.render_mode import RenderMode
from yakoon.solution.platform.registry import SolutionRegistry
from yakoon.solution.settings import SolutionSettings

# Set the global rendering mode to ansi text (no Markdown formatting)
SolutionSettings.runtime.render_mode = RenderMode.PLAIN

output_buffer = OutputBufferManager()

session_id = "cli"


async def msg(text: str):
    await output_buffer.collect(session_id, text)

async def err(text: str):
    await output_buffer.collect(session_id, f"⚠️: {text}")


async def run_console():
   
    engine = Engine(SolutionRegistry())

    asyncio.create_task(engine.send(session_id, "batch: login stefan; switch mud;", msg, err))
    #print(await output_buffer.flush_when_ready(session_id))

    while True:
        command = await ainput("|:> ")

        # Prompt-Antwort?
        if DialogManager.resolve_prompt(session_id, command):
            print(await output_buffer.flush_when_ready(session_id))
            continue

        asyncio.create_task(engine.send(session_id, command, msg, err))

        # Prompt wurde vielleicht jetzt aktiviert?
        await asyncio.sleep(0)  # Yield, damit async msg() greifen kann
        if DialogManager.is_waiting(session_id):
            print(await output_buffer.flush_when_ready(session_id))
            continue

        # Normale Ausgabe
        print(await output_buffer.flush_when_ready(session_id))

if __name__ == "__main__":
    asyncio.run(run_console())