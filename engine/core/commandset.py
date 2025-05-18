from typing import Protocol, Sequence, Type

from engine.core.command import Command

class CommandSet(Protocol):
    
    @staticmethod
    def commands() -> Sequence[Type[Command]]: ...

    @staticmethod
    def build_command_set(commands: list[Type[Command]]):
        class InlineCommandSet:
            @staticmethod
            def commands() -> Sequence[Type[Command]]:
                return commands
        return InlineCommandSet