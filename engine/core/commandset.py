from typing import Protocol, Sequence, Type

from engine.core.command import Command

class CommandSet(Protocol):
    
    @staticmethod
    def commands() -> Sequence[Type[Command]]: ...