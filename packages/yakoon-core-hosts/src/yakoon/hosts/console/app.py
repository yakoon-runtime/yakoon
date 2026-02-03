import asyncio


from yakoon.auth.controller import AuthCoreController
from yakoon.base.models.key import Key
from yakoon.base import ports 
from yakoon.base.utils.format import format_prompt
from yakoon.base.utils.input import safe_input, safe_input_secret
from yakoon.base.runtime.devtools import MemoryTrendMonitor
from yakoon.base.runtime.devtools import UnresolvedPromptMonitor
from yakoon.base.runtime.session.output import Output

from yakoon.platform.runtime.dialogs.manager import DialogManager, PromptMode
from yakoon.platform.settings import settings
from yakoon.platform.runtime.render.mode import RenderMode
from yakoon.platform.directories.controller import ControllerDirectory
from yakoon.compose.engine import compose_engine

from yakoon.shell.controller import ShellCoreController
from yakoon.office.mailing.controller import OfficeMailingCoreController


# Set the global rendering mode to ansi text (no Markdown formatting)
settings.render.render_mode = RenderMode.PLAIN

command_inits = ["welcome"]
#command_inits += ["use auth", "su", "exit"]


async def run_console():
   
    session = None
    output = Output(print, print)
    session_key = Key.from_parts("yakoon", "bucket", "develop", "cli")

    engine = await compose_engine(
        controllers=ControllerDirectory(
            controllers=[
                ShellCoreController(), 
                AuthCoreController(),
                OfficeMailingCoreController()]))

    await engine.initialize(output)

    queue = engine._services.get(ports.CommandQueueService)
    
    while True:

        prompt = format_prompt(session)

        if session and DialogManager.is_waiting(session):
            mode = DialogManager.get_mode(session)
            if mode == PromptMode.SECRET:
                command = await safe_input_secret(prompt=prompt)
            else:
                command = await safe_input(prompt=prompt)

        elif command_inits:
            command = command_inits.pop(0).strip()

        else:
            command = queue.next_command(session) if session else None
            if command == None:
                command = await safe_input(prompt=prompt)

        session = await engine.dispatch(session_key, command, output)

if __name__ == "__main__":    
   asyncio.run(run_console())
