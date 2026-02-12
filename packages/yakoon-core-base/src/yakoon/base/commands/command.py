from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Optional

from yakoon.base.ports import NamespaceService, Presenter, PresenterService
from yakoon.base.models.command import CommandKind, CommandVisibility
from yakoon.base.models.ns import Namespace
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session.session import Session
from yakoon.base.directories.service import ServiceDirectory
from yakoon.base.controllers.base import BaseController


class CmdNotFound(Exception):
    pass


@dataclass(frozen=True)
class CommandContext:
    controller: BaseController
    batch_id: Optional[str] = None

    @property
    def is_batch(self):
        return bool(self.batch_id)

class Command(ABC):

    key: str
    aliases: list[str] = []
    context: CommandContext 

    template_prefix: str = ""
    controller: BaseController = None

    kind: CommandKind = CommandKind.USER
    visibility: CommandVisibility = CommandVisibility.NORMAL
   
    @property
    def services(self) -> ServiceDirectory:
        return self.context.controller.services

    def get_template_path(self) -> str:
        template_sub_path = self.context.controller.template_source.template_sub_path
        return str(Path(template_sub_path).joinpath(self.template_prefix, self.key))

    async def get_namespace(self, session) -> Namespace:
        namespaces = self.services.get(NamespaceService)   

        return await namespaces.from_session(session)

    async def get_presenter(self, session) -> Presenter:
        presenter = self.services.get(PresenterService) 
        
        return await presenter.create_presenter(
                self.context.controller.template_source.package,
                self.get_template_path(), session)
                
    async def run(self, session: Session, request: Request):
        pass
