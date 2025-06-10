from yakoon.saas.engines.command import Engine, Output
from yakoon.mesh.runtime.render.models.mode import RenderMode
from yakoon.saas.controllers.gateway.utils.ansi import format_codes_to_ansi
from yakoon.saas.bootstrap.registry import BootstrapControllerDirectory
from yakoon.saas.bootstrap.settings import SolutionSettings


# Set the global rendering mode to ansi text (no Markdown formatting)
SolutionSettings.runtime.render_mode = RenderMode.ANSI
engine = Engine(BootstrapControllerDirectory())


async def handle_client(reader, writer):

    async def out(msg: str):
        msg_str = format_codes_to_ansi(str(msg))  
        writer.write((msg_str + "\r\n").encode("utf-8"))  
        await writer.drain()

    addr = writer.get_extra_info("peername")
    session_id = f"{addr[0]}:{addr[1]}"
    print(f"[Telnet] Verbindung von {session_id}")
    
    await engine.initialize(Output(out, out))

    while True:
        command = await reader.readline()
        if not command:
            continue            
        command = command.decode("utf-8").strip()
        await engine.dispatch(session_id, command, Output(out, out))