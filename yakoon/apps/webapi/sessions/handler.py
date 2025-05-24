# yakoon/app/webapi/session_manager.py

from yakoon.engine.core.registry import DomainRegistry
from yakoon.engine.runtime import Engine
from yakoon.domains.game.controller import GameController
from yakoon.platform.controller import PlatformController
from yakoon.platform.runtime.session import PlatformSession
from yakoon.platform.services.session_service import SessionService
from yakoon.platform.stores.memory_session_store import InMemorySessionStore


sessions = SessionService(
    store=InMemorySessionStore(session_cls=PlatformSession))

registry = DomainRegistry(
    controllers=[
        GameController(),
    ],
    system=PlatformController(),
    sessions=sessions,
    )

_engine = Engine(registry)


async def handle_input(session_id: str, input_str: str) -> str:
    output: list[str] = []

    async def collector(msg: str):
        output.append(str(msg))

    await _engine.send(session_id, input_str, collector, collector)
    return "\n".join(output)
