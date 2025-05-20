# yakoon/app/telnet/session_bridge.py

from yakoon.engine.runtime import Engine
from yakoon.game.definition import GameDefinition
from yakoon.game.runtime.session import GameSession

_engine = Engine(GameDefinition)


async def handle_telnet_session(reader, writer):
   
    addr = writer.get_extra_info("peername")
    session_id = f"{addr[0]}:{addr[1]}"
    print(f"🧩 Telnet-Session: {session_id}")

    #output: list[str] = []

    async def out(msg: str):
        writer.write((msg + "\r\n").encode("utf-8"))
        await writer.drain()

    async def on_ready(session: GameSession):
        while True:
            line = await reader.readline()
            if not line:
                break
            input_str = line.decode().strip()
            await _engine.send(session, input_str)

    await _engine.enter(session_id, out, out, on_ready)
