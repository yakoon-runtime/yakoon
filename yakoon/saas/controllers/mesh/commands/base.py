
from yakoon.saas.commands.command import SaasCommand


class MeshCommand(SaasCommand):

    async def get_template_path(self) -> str:
        return f"gateway/commands/{self.template_key}"
    