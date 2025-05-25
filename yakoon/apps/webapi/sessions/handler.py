# yakoon/app/webapi/session_manager.py

from yakoon.engine.runtime import Engine
from yakoon.solution.platform.registry import SolutionRegistry


_engine = Engine(SolutionRegistry())


async def handle_input(session_id: str, input_str: str) -> str:
    output: list[str] = []

    async def collector(msg: str):
        output.append(str(msg))

    await _engine.send(session_id, input_str, collector, collector)
    return "\n".join(output)
