from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

from typing import TYPE_CHECKING
from yakoon.base.models.namespace import Namespace
from yakoon.base.runtime.views.presenter import Presenter
from yakoon.base.runtime.system.registry import ServiceRegistry

if TYPE_CHECKING:
    from yakoon.base.controllers.base import BaseController


class CmdNotFound(Exception):
    pass


class MeshCommand(ABC):

    key: str
    aliases: list[str] = []
    template_key: str = ""

    controller: BaseController = None
   
    @abstractmethod
    async def run(self, session: Any, request: Any) -> None | RemoteDispatchResult:
        pass

    @abstractmethod
    async def get_template_path(self) -> str:
        pass

    async def get_namespace(self, session) -> Namespace:
        services = await self.get_system_services()
        return await services.namespaces.from_session(session)

    async def get_presenter(self, session) -> Presenter:
        services = await self.get_system_services()
        return Presenter(await self.get_template_path(), session, renderer=services.renderer)
        
    async def get_services(self) -> ServiceRegistry:
        return await self.controller.get_domain_services()
