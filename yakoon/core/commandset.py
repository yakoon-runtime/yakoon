from __future__ import annotations
from typing import Protocol, Sequence, Type

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from yakoon.core.command import Command


class CommandSet(Protocol):
    
    category: str = "unnamed"

    @staticmethod
    def commands() -> Sequence[Type[Command]]: ...

    @staticmethod
    def build_command_set(commands: list[Type[Command]]):
        class InlineCommandSet:
            @staticmethod
            def commands() -> Sequence[Type[Command]]:
                return commands
        return InlineCommandSet