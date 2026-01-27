
from yakoon.platform.commands.command import SaasCommand


class PlatformCommand(SaasCommand):

    async def get_template_path(self) -> str:
        return f"gateway/commands/{self.template_key}"