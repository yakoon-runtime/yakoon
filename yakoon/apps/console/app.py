
import asyncio
from aioconsole import ainput
from yakoon.engine.core.registry import DomainRegistry
from yakoon.engine.runtime import Engine
from yakoon.platform.services.session_service import SessionService
from yakoon.platform.stores.memory_session_store import InMemorySessionStore
from yakoon.solution.controller import SolutionMainController
from yakoon.solution.domains.game.controller import SolutionGameController
from yakoon.solution.platform.runtime.session import Session


async def err(exc: Exception):
    print(exc)


async def msg(text: str):
    print(text)


async def run_console():

    sessions = SessionService(
        store=InMemorySessionStore(session_cls=Session))
   
    registry = DomainRegistry(
        controllers=[
            SolutionGameController(),
        ],
        system=SolutionMainController(),
        sessions=sessions,
        )
  
    session_id = "cli"
    engine = Engine(registry)

    asyncio.create_task(engine.send(session_id, "batch: login stefan; switch mud; help", msg, err))
    while True:
        command = await ainput("|:> ")
        asyncio.create_task(engine.send(session_id, command, msg, err))

if __name__ == "__main__":
    asyncio.run(run_console())