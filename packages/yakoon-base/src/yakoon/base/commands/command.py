from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

from yakoon.base.models.namespace import Namespace
from yakoon.base.runtime.views.presenter import Presenter
from yakoon.base.runtime.system.registry import ServiceRegistry
from yakoon.base.controllers.base import BaseController


class CmdNotFound(Exception):
    pass


class Command(ABC):

    key: str
    aliases: list[str] = []
    template_key: str = ""

    controller: BaseController = None
   
    async def get_template_path(self) -> str:
        return self.template_key

    async def get_namespace(self, session) -> Namespace:
        services = await self.get_services()
        namespaces = await services.get("namespaces")
        
        return await namespaces.from_session(session)

    async def get_presenter(self, session) -> Presenter:
        services = await self.get_services()
        renderer = await services.get("renderer")

        return Presenter(await self.get_template_path(), session, renderer=renderer)
        
    async def get_services(self) -> ServiceRegistry:
        return self.controller.services
