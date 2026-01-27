from __future__ import annotations

from yakoon.base.commands.command import MeshCommand
from yakoon.base.controllers.base.directory import BaseControllerDirectory
from yakoon.platform.controllers.gateway.services._registry import GatewayServiceRegistry
from yakoon.platform.services._registry import SystemServiceRegistry


class SaasCommand(MeshCommand):

    async def get_controller_directory(self) -> BaseControllerDirectory:
        return await self.controller.get_controller_directory()
        
    async def get_gateway_services(self) -> GatewayServiceRegistry:
        return await self.controller.get_gateway_services()
    
    async def get_system_services(self) -> SystemServiceRegistry:
        return await self.controller.get_system_services()
