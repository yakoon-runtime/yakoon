from __future__ import annotations
from abc import ABC
from pathlib import Path

from yakoon.base.ports import CommandInvokerService, NamespaceService, Presenter, PresenterService
from yakoon.base.commands.request import Request
from yakoon.base.models.namespace import Namespace
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
        sub_template_path = self.controller.template_source.sub_template_path
        return str(Path(sub_template_path).joinpath(self.template_prefix, self.key))

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


class BatchCommand(Command):

    async def run(self, session: Session, request: Request):

        raw = request.raw
        invoker = self.services.get(CommandInvokerService)

        # minimal split - quoting later...
        parts = [p.strip() for p in raw.split(";") if p.strip()]

        for cmd in parts:
            ok = await invoker.invoke_text(session, cmd)
            if not ok:
                break