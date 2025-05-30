
from yakoon.engine.core.command import Command
from yakoon.platform.render.context import Presenter


class PlatformCommand(Command):

    async def get_template_path(self) -> str:
        return f"platform/commands/{self.template_key}"
    
    async def get_presenter(self, session) -> Presenter:
        return Presenter(await self.get_template_path(), session)