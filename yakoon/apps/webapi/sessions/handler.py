# yakoon/app/webapi/session_manager.py

from yakoon.engine.core.io.adapter import IOAdapter
from yakoon.engine.runtime import Engine
from yakoon.platform.render.engine.mode import RenderMode
from yakoon.solution.platform.registry import SolutionRegistry
from yakoon.solution.settings import SolutionSettings


# Set the global rendering mode to ansi text (no Markdown formatting)
SolutionSettings.runtime.render_mode = RenderMode.MARKDOWN
_engine = Engine(SolutionRegistry())


async def handle_input(session_id: str, input_str: str) -> str:
    output: list[str] = []

    async def out(msg: str):
        output.append(str(msg))

    io = IOAdapter(out, out)

    await _engine.send(session_id, input_str, io)
    return "\n".join(output)
