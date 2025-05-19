from abc import ABC, abstractmethod
from typing import Sequence, Type
from engine.core.commandset import CommandSet


class BaseGameDefinition(ABC):

    session_cls = None
    default_command_groups = []     

    @property
    @abstractmethod
    def commandsets(self) -> Sequence[Type[CommandSet]]: ...

    async def on_before_run_command(session, request, command):
        pass
    async def on_after_run_command(session, request, command):
        pass

