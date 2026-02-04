import asyncio
from uuid import uuid4

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
   
    session_key = Key.from_parts("yakoon", "bucket", "develop", "1",)
    
    engine = await compose_engine(
        controllers=ControllerDirectory(
            controllers=[
                ShellCoreController(), 
                AuthCoreController(),
                OfficeMailingCoreController()]))

    queue = engine.services.get(ports.CommandQueueService)
    sessions = engine.services.get(ports.SessionService)
    session, _ = await sessions.get_or_create(session_key)
    session.bind_io(Output(print, print))

    queue.enqueue_commands(session, command_inits)

    try:
        while True:

            prompt = format_prompt(session)

            if DialogManager.is_waiting(session):
                mode = DialogManager.get_mode(session)
                if mode == PromptMode.SECRET:
                    command = await safe_input_secret(prompt=prompt)
                else:
                    command = await safe_input(prompt=prompt)

            else:
                command = queue.next_command(session)
                if command is None:
                    command = await safe_input(prompt=prompt)

            await engine.dispatch(session, command)
            if session.has_signal("exit_app"):
                break  
    finally:
        sessions.release(session.key)


if __name__ == "__main__":    
   asyncio.run(run_console())
