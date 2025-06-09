
from yakoon.saas.commands.command import Command


class MeshCommand(Command):

    async def get_template_path(self) -> str:
        return f"gateway/commands/{self.template_key}"
    