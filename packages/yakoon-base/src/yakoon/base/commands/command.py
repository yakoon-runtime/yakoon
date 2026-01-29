from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

from yakoon.base.models.namespace import Namespace
from yakoon.base.runtime.views.presenter import Presenter
from yakoon.base.runtime.system.registry import NewServiceRegistry
from yakoon.base.controllers.base import BaseController


class CmdNotFound(Exception):
    pass


class MeshCommand(ABC):

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

    async def get_namespace(self, session) -> Namespace:
        services = await self.get_services()
        namespaces = await services.get("namespaces")
        
        return await namespaces.from_session(session)

    async def get_presenter(self, session) -> Presenter:
        services = await self.get_services()
        renderer = await services.get("renderer")

        return Presenter(await self.get_template_path(), session, renderer=renderer)
        
    async def get_services(self) -> NewServiceRegistry:
        return self.controller.services
