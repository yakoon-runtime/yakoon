
from yakoon.saas.commands.command import SaasCommand


class LoopCommand(SaasCommand):

    async def get_template_path(self) -> str:
        return f"gateway/commands/{self.template_key}"