from yakoon.engine.runtime import Engine
from yakoon.platform.render.render_mode import RenderMode
from yakoon.platform.utils.ansi import format_codes_to_ansi
from yakoon.solution.platform.registry import SolutionRegistry
from yakoon.solution.settings import SolutionSettings


# Set the global rendering mode to ansi text (no Markdown formatting)
SolutionSettings.runtime.render_mode = RenderMode.ANSI
_engine = Engine(SolutionRegistry())


async def handle_client(reader, writer):

    addr = writer.get_extra_info("peername")
    session_id = f"{addr[0]}:{addr[1]}"
    print(f"[Telnet] Verbindung von {session_id}")

    async def out(msg: str):
        msg_str = format_codes_to_ansi(str(msg))  
        writer.write((msg_str + "\r\n").encode("utf-8"))  
        await writer.drain()

    await out("|wWillkommen bei Yakoon!|n")  
    while True:
        command = await reader.readline()
        if not command:
            break
        await _engine.send(session_id, command.decode("utf-8").strip(), out, out)