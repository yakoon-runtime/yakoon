from abc import ABC, abstractmethod
from typing import Sequence, Type
from engine.core.commandset import CommandSet


class BaseGameDefinition(ABC):

    @property
    @abstractmethod
    def commandsets(self) -> Sequence[Type[CommandSet]]: ...

    @property
    @abstractmethod
    def room_store(self): ...
