
from yakoon.core.command import Command
from yakoon.domains.platform.render.context import Presenter
from yakoon.domains.platform.runtime.session import PlatformSession
from yakoon.domains.platform.services.registry import PlatformServiceRegistry


class PlatformCommand(Command):

    async def get_template_path(self) -> str:
        return f"platform/commands/{self.template_key}"
    
    async def get_presenter(self, session: PlatformSession) -> Presenter:
        return Presenter(await self.get_template_path(), session)
    
    async def get_services(self, session: PlatformSession) -> PlatformServiceRegistry:
        return session.ctx.gateway.services.get_registry("gateway")
        
