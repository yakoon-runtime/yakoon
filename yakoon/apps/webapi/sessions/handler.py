# yakoon/app/webapi/session_manager.py

import asyncio
from yakoon.engine.core.dialog.manager import DialogManager
from yakoon.engine.core.tools.output import OutputBufferManager
from yakoon.engine.runtime import Engine
from yakoon.platform.render.render_mode import RenderMode
from yakoon.solution.platform.registry import SolutionRegistry
from yakoon.solution.settings import SolutionSettings


# Set the global rendering mode to ansi text (no Markdown formatting)
SolutionSettings.runtime.render_mode = RenderMode.MARKDOWN

engine = Engine(SolutionRegistry())
output_buffer = OutputBufferManager()


async def handle_input(session_id: str, input_str: str) -> str:

    async def collector(msg: str):
        await output_buffer.collect(session_id, msg)

    # Phase 1: Prompt-Antwort?
    if DialogManager.resolve_prompt(session_id, input_str):
        return await output_buffer.flush_when_ready(session_id)

    # Phase 2: Normaler Befehl (nicht blockieren!)
    asyncio.create_task(
        engine.send(session_id, input_str, collector, collector))

    # Phase 3: Ist `ask()` aktiv geworden? (nach kurzem Yield)
    await asyncio.sleep(0)  # wichtig!
    if DialogManager.is_waiting(session_id):
        return await output_buffer.flush_when_ready(session_id)

    # Phase 4: Kein Dialog – normale Ausgabe
    return await output_buffer.flush_when_ready(session_id)
    