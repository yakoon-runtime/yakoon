from yakoon.apps.telnet.utils.translate import translate_ansi
from yakoon.engine.runtime import Engine
from yakoon.domains.game.controller import GameController


_engine = Engine(GameController)


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