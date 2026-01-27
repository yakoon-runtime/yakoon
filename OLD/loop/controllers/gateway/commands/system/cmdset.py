from typing import Sequence, Type
from yakoon.loop.runtime.commands.command import MeshCommand
from yakoon.loop.runtime.commands.commandset import CommandSet
from yakoon.loop.controllers.gateway.commands.system.cmd_welcome import CmdWelcome


class MeshSystemCommands(CommandSet):
    
    category = "System"

    @classmethod
    def commands(cls) -> Sequence[Type[MeshCommand]]: 
        return [
            CmdWelcome,
        ]