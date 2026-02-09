from __future__ import annotations
from abc import ABC
from pathlib import Path

from yakoon.base.ports import NamespaceService, Presenter, PresenterService
from yakoon.base.commands.request import Request
from yakoon.base.models.ns import Namespace
from yakoon.base.runtime.session.session import Session
from yakoon.base.directories.service import ServiceDirectory
from yakoon.base.controllers.base import BaseController


class CmdNotFound(Exception):
    pass


class Command(ABC):

    key: str
    aliases: list[str] = []

    template_prefix: str = ""
    controller: BaseController = None
   
    @property
    def services(self) -> ServiceDirectory:
        return self.controller.services

    def get_template_path(self) -> str:
        template_sub_path = self.controller.template_source.template_sub_path
        return str(Path(template_sub_path).joinpath(self.template_prefix, self.key))

    async def get_namespace(self, session) -> Namespace:
        namespaces = self.services.get(NamespaceService)   

        return await namespaces.from_session(session)

    async def get_presenter(self, session) -> Presenter:
        presenter = self.services.get(PresenterService) 
        
        return await presenter.create_presenter(
                self.controller.template_source.package,
                self.get_template_path(), session)
                
    async def run(self, session: Session, request: Request):
        pass
