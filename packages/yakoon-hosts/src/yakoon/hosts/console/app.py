import asyncio

from yakoon.base.models.key import Key
from yakoon.base.runtime.devtools import MemoryTrendMonitor
from yakoon.base.runtime.devtools import UnresolvedPromptMonitor
from yakoon.base.runtime.session.output import Output
from yakoon.base.utils.input import safe_input

from yakoon.platform.settings import settings
from yakoon.platform.runtime.render.models.mode import RenderMode
from yakoon.platform.controllers.directory import ControllerDirectory
from yakoon.platform.controllers.gateway.controller import GatewayController

from yakoon.compose.build import compose_engine


# Set the global rendering mode to ansi text (no Markdown formatting)
settings.render.render_mode = RenderMode.PLAIN

command_inits = ["welcome"]
#command_inits += ["batch: login stefan; switch; realm; ic stefan; version; switch;"]
#command_inits += ["batch: login Stefan; switch realm; ic Stefan"]
#command_inits += ["batch: login Stefan; switch mesh"]
#command_inits += ["ping"]

async def run_console():
   
   output = Output(print, print)

   engine = await compose_engine(
      controllers=ControllerDirectory(
         controllers=[GatewayController()]))

   await engine.initialize(output)
   
   session = Key.from_parts("yakoon", "bucket", "develop", "cli")
   while True:                       
      command = (command_inits.pop(0).strip() 
         if command_inits else await safe_input())
      await engine.dispatch(session, command, output)

if __name__ == "__main__":    
   asyncio.run(run_console())
