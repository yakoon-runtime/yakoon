from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

from typing import TYPE_CHECKING

from yakoon.saas.models.namespace import Namespace
from yakoon.saas.controllers.directory import BaseControllerDirectory
from yakoon.saas.controllers.gateway.services._registry import GatewayServiceRegistry
from yakoon.saas.runtime.views.presenter import Presenter
from yakoon.saas.runtime.system.registry import ServiceRegistry
from yakoon.saas.services._registry import SystemServiceRegistry

if TYPE_CHECKING:
    from yakoon.saas.controllers.base import BaseController


class CmdNotFound(Exception):
    pass

class Command(ABC):

    key: str
    aliases: list[str] = []
    template_key: str = ""

    controller: BaseController = None
   
    @abstractmethod
    async def run(self, session: Any, request: Any) -> None:
        pass

    @abstractmethod
    async def get_template_path(self) -> str:
        pass

    async def get_controller_directory(self) -> BaseControllerDirectory:
        return await self.controller.get_controller_directory()

    async def get_namespace(self, session) -> Namespace:
        services = await self.get_system_services()
        return await services.namespaces.from_session(session)

    async def get_presenter(self, session) -> Presenter:
        services = await self.get_system_services()
        return Presenter(await self.get_template_path(), session, renderer=services.renderer)
        
    async def get_domain_services(self) -> ServiceRegistry:
        return await self.controller.get_domain_services()

    async def get_gateway_services(self) -> GatewayServiceRegistry:
        return await self.controller.get_gateway_services()
    
    async def get_system_services(self) -> SystemServiceRegistry:
        return await self.controller.get_system_services()
