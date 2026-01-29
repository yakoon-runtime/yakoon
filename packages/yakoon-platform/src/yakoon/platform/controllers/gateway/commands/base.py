
from yakoon.base.commands.command import MeshCommand


class PlatformCommand(MeshCommand):

    async def get_template_path(self) -> str:
        return f"gateway/commands/{self.template_key}"