from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Sequence, Type

from yakoon.engine.core.commandset import CommandSet
from yakoon.engine.core.parser import Request
from yakoon.engine.services.session_service import BaseSessionService

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yakoon.engine.system.session import BaseSession
    from yakoon.engine.core.command import Command


class DomainDefinition(ABC):

    default_command_groups = []     
    sessions: BaseSessionService

    @property
    @abstractmethod
    def commandsets(self) -> Sequence[Type[CommandSet]]: ...

    async def on_before_send(self, session: BaseSession):
        pass

    async def on_before_run_command(self, 
                                    session: BaseSession, 
                                    request: Request, 
                                    command: Command):
        pass
    
    async def on_after_run_command(self, 
                                   session: BaseSession, 
                                   request: Request, 
                                   command: Command):
        pass
    
    async def on_after_send(self, session: BaseSession):
        pass

