# yakoon/app/webapi/session_manager.py
from yakoon.engine import Engine, Output
from yakoon.services.renderer import RenderMode
from yakoon.solution.registry import SolutionRegistry
from yakoon.solution.settings import SolutionSettings


# Set the global rendering mode to ansi text (no Markdown formatting)
SolutionSettings.runtime.render_mode = RenderMode.MARKDOWN
_engine = Engine(SolutionRegistry())


async def handle_input(session_id: str, input_str: str) -> str:
    output: list[str] = []

    async def out(msg: str):
        output.append(str(msg))

    output = Output(out, out)

    await _engine.send(session_id, input_str, output)
    return "\n".join(output)
