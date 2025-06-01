
from yakoon.core.command import Command


class PlatformCommand(Command):

    async def get_template_path(self) -> str:
        return f"platform/commands/{self.template_key}"