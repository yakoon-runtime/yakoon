import asyncio


from yakoon.base.models.key import Key
from yakoon.base.utils.input import safe_input
from yakoon.base.runtime.devtools import MemoryTrendMonitor
from yakoon.base.runtime.devtools import UnresolvedPromptMonitor
from yakoon.base.runtime.session.output import Output

from yakoon.platform.settings import settings
from yakoon.platform.runtime.render.mode import RenderMode
from yakoon.platform.directories.controller import ControllerDirectory
from yakoon.compose.engine import compose_engine

from yakoon.shell.controller import ShellController
from yakoon.office.mailing.controller import OfficeMailingController


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
         controllers=[ShellController(), OfficeMailingController()]))

   await engine.initialize(output)
   
   while True:                       
      prefix = session.get_active_controller("") if session else ""   
      command = (command_inits.pop(0).strip() 
         if command_inits else await safe_input(prefix=prefix))
      session = await engine.dispatch(session_key, command, output)

if __name__ == "__main__":    
   asyncio.run(run_console())
