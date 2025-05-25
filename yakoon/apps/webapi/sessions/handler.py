# yakoon/app/webapi/session_manager.py

from yakoon.engine.runtime import Engine
from yakoon.platform.render.render_mode import RenderMode
from yakoon.solution.platform.registry import SolutionRegistry
from yakoon.solution.settings import SolutionSettings


# Set the global rendering mode to ansi text (no Markdown formatting)
SolutionSettings.runtime.render_mode = RenderMode.MARKDOWN
_engine = Engine(SolutionRegistry())


async def handle_input(session_id: str, input_str: str) -> str:
    output: list[str] = []

    async def collector(msg: str):
        output.append(str(msg))

    await _engine.send(session_id, input_str, collector, collector)
    return "\n".join(output)
