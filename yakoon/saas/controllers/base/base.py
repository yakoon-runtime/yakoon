from __future__ import annotations
from typing import TYPE_CHECKING

from yakoon.mesh.controllers.base.base import BaseController
from yakoon.mesh.runtime.system.registry import ServiceRegistry
from yakoon.saas.engines.command.router import CommandRouter

if TYPE_CHECKING:
    from yakoon.mesh.controllers.base.directory import BaseControllerDirectory
    from yakoon.saas.commands.command import SaasCommand
    

class SaasBaseController(BaseController):
    """
    Abstract base for all domain/platform definitions.
    Provides router and default session/command group config.
    """

    def __init__(self):
        super().__init__()
        self.router = CommandRouter()
        self._register_all_commands()

    def _register_all_commands(self):
        for commands_set in self.commandsets:
            category = getattr(commands_set, "category", "system")
            self.router.register(self._get_value_with_prefix(category), commands_set)

    def resolve(self, name: str, cmd_groups: list[str] | None = None) -> SaasCommand | None:
        return self.router.resolve(name, cmd_groups)

    async def get_gateway_services(self) -> ServiceRegistry:
        if self.gateway is None or self.gateway.id == self.id:
            return await self.service_router.get_registry(self.id)
        return await self.gateway.service_router.get_registry(self.gateway.id)

    async def get_controller_directory(self) -> BaseControllerDirectory:
        gateway = self.gateway if self.gateway else self 
        if hasattr(gateway, "controller_directory"):
            return gateway.controller_directory
        return None
