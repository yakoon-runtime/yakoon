from __future__ import annotations

from yakoon.mesh.commands.command import MeshCommand
from yakoon.saas.controllers.directory import BaseControllerDirectory
from yakoon.saas.controllers.gateway.services._registry import GatewayServiceRegistry
from yakoon.saas.services._registry import SystemServiceRegistry


class SaasCommand(MeshCommand):

    async def get_controller_directory(self) -> BaseControllerDirectory:
        return await self.controller.get_controller_directory()
        
    async def get_gateway_services(self) -> GatewayServiceRegistry:
        return await self.controller.get_gateway_services()
    
    async def get_system_services(self) -> SystemServiceRegistry:
        return await self.controller.get_system_services()
