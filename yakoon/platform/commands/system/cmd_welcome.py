from yakoon.engine.core.command import Command
from yakoon.engine.core.parser import Request
from yakoon.platform.render.context import Presenter
from yakoon.platform.runtime.session import PlatformSession
from yakoon.plugins.ai.agent import ask_AI


class CmdWelcome(Command):

    key = "welcome"    
    requires = ["system"]

    async def run(self, session: PlatformSession, request: Request):

        presenter = Presenter("commands/system/cmd_welcome", session)
        await presenter.emit("show")