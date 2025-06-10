from __future__ import annotations
from typing import Protocol, Sequence, Type

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from yakoon.mesh.commands.command import MeshCommand


class CommandSet(Protocol):
    
    category: str = "unnamed"

    @staticmethod
    def commands() -> Sequence[Type[MeshCommand]]: ...

    @staticmethod
    def build_command_set(commands: list[Type[MeshCommand]]):
        class InlineCommandSet:
            @staticmethod
            def commands() -> Sequence[Type[MeshCommand]]:
                return commands
        return InlineCommandSet