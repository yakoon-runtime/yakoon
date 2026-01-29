
from yakoon.base.commands.command import Command


class PlatformCommand(Command):

    async def get_template_path(self) -> str:
        return f"gateway/commands/{self.template_key}"