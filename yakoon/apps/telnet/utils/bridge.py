from yakoon.apps.telnet.utils.translate import translate_ansi
from yakoon.engine.core.registry import DomainRegistry
from yakoon.engine.runtime import Engine
from yakoon.platform.services.session_service import SessionService
from yakoon.platform.stores.memory_session_store import InMemorySessionStore
from yakoon.solution.controller import SolutionMainController
from yakoon.solution.domains.game.controller import SolutionGameController
from yakoon.solution.platform.runtime.session import Session


sessions = SessionService(
    store=InMemorySessionStore(session_cls=Session))

registry = DomainRegistry(
    controllers=[
        SolutionGameController(),
    ],
    system=SolutionMainController(),
    sessions=sessions,
    )

_engine = Engine(registry)


async def handle_client(reader, writer):

    addr = writer.get_extra_info("peername")
    session_id = f"{addr[0]}:{addr[1]}"
    print(f"[Telnet] Verbindung von {session_id}")

    async def out(msg: str):
        msg_str = translate_ansi(str(msg))  
        writer.write((msg_str + "\r\n").encode("utf-8"))  
        await writer.drain()

    async def on_ready(session):
        await out("|wWillkommen bei Yakoon!|n")  
        while True:
            line = await reader.readline()
            if not line:
                break
            await _engine.send(session, line.decode("utf-8").strip())

    await _engine.enter(session_id, out, out, on_ready)