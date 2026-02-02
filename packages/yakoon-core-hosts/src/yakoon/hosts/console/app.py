import asyncio


from yakoon.auth.controller import AuthCoreController
from yakoon.base.models.key import Key
from yakoon.base.utils.input import safe_input, safe_input_secret
from yakoon.base.runtime.devtools import MemoryTrendMonitor
from yakoon.base.runtime.devtools import UnresolvedPromptMonitor
from yakoon.base.runtime.session.output import Output

from yakoon.platform.runtime.dialogs.manager import DialogManager
from yakoon.platform.settings import settings
from yakoon.platform.runtime.render.mode import RenderMode
from yakoon.platform.directories.controller import ControllerDirectory
from yakoon.compose.engine import compose_engine

from yakoon.shell.controller import ShellCoreController
from yakoon.office.mailing.controller import OfficeMailingCoreController


# Set the global rendering mode to ansi text (no Markdown formatting)
settings.render.render_mode = RenderMode.PLAIN

command_inits = ["welcome"]
#command_inits += ["batch: login stefan; switch; realm; ic stefan; version; switch;"]
#command_inits += ["batch: login Stefan; switch realm; ic Stefan"]
#command_inits += ["batch: login Stefan; switch mesh"]
#command_inits += ["ping"]

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
   
   while True:
    prefix = session.get_active_controller("") if session else ""

    if command_inits:
        command = command_inits.pop(0).strip()
    else:
        if session and DialogManager.is_waiting(session):
            mode = DialogManager.get_mode(session)
            if mode == "secret":
                command = await safe_input_secret(prefix=prefix)
            else:
                command = await safe_input(prefix=prefix)
        else:
            command = await safe_input(prefix=prefix)

    session = await engine.dispatch(session_key, command, output)


if __name__ == "__main__":    
   asyncio.run(run_console())
