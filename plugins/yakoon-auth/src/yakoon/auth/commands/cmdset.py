from typing import Sequence, Type
from yakoon.base.commands.command import Command
from yakoon.base.commands.commandset import CommandSet

from yakoon.auth.commands.cmd_su import CmdSu

class AuthSystemCommands(CommandSet):
    
    category = "system"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdSu,
        ]