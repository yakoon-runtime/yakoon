from yakoon.engine.core.parser import Request
from yakoon.platform.commands.command import PlatformCommand
from yakoon.platform.runtime.session import PlatformSession
from yakoon.plugins.ai.agent import ask_AI


class CmdWelcome(PlatformCommand):

    key = "welcome"    
    requires = ["system"]

    async def run(self, session: PlatformSession, request: Request):
        await session.out("Yakoon sagt: 'Willkommen'.")

        #result = await ask_AI("Sag Hallo.")
        #await session.out(result)