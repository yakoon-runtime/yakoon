# yakoon/app/webapi/session_manager.py

from yakoon.engine.runtime import Engine
from yakoon.game.definition import GameDefinition
from yakoon.game.runtime.session import GameSession


_engine = Engine(GameDefinition)


async def handle_input(session_id: str, input_str: str) -> str:
    output: list[str] = []

    async def collector(msg: str):
        output.append(str(msg))

    async def on_ready(session: GameSession):
        return await _engine.send(session, input_str) 

    await _engine.enter(session_id, collector, collector, on_ready)
    return "\n".join(output)
