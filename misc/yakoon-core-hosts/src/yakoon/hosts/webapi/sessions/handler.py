# yakoon/app/webapi/session_manager.py
from yakoon.platform.engines.command import Engine, Output
from yakoon.base.runtime.render.models.mode import RenderMode
from yakoon.platform.bootstrap.settings import SolutionSettings


# Set the global rendering mode to ansi text (no Markdown formatting)
SolutionSettings.runtime.render_mode = RenderMode.MARKDOWN
_engine = Engine(None)


async def handle_input(session_id: str, input_str: str) -> str:
    output: list[str] = []

    async def out(msg: str):
        output.append(str(msg))

    output = Output(out, out)

    await _engine.send(session_id, input_str, output)
    return "\n".join(output)
