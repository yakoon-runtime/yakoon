from yakoon.engine.core.parser import Request
from yakoon.platform.commands.base import PlatformCommand
from yakoon.platform.runtime.session import PlatformSession


class CmdWelcome(PlatformCommand):

    key = "welcome"    
    template_key = "system/cmd_welcome"

    requires = ["system"]

    async def run(self, session: PlatformSession, _: Request):

        await self.get_presenter(session).emit("show")