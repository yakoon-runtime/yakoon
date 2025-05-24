
import asyncio
from aioconsole import ainput
from yakoon.domains.game.controller import GameController
from yakoon.engine.core.registry import DomainRegistry
from yakoon.engine.runtime import Engine
from yakoon.platform.controller import PlatformController
from yakoon.platform.runtime.session import PlatformSession
from yakoon.platform.services.session_service import SessionService
from yakoon.platform.stores.memory_session_store import InMemorySessionStore


async def err(exc: Exception):
    print(exc)


async def msg(text: str):
    print(text)


async def run_application():

    sessions = SessionService(
        store=InMemorySessionStore(session_cls=PlatformSession))
   
    registry = DomainRegistry(
        controllers=[
            GameController(),
        ],
        system=PlatformController(),
        sessions=sessions,
        )
  
    session_id = "cli"
    engine = Engine(registry)

    asyncio.create_task(engine.send(session_id, "batch: login stefan; switch mud; help", msg, err))
    while True:
        command = await ainput("|:> ")
        asyncio.create_task(engine.send(session_id, command, msg, err))

if __name__ == "__main__":
    asyncio.run(run_application())