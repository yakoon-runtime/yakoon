from typing import Sequence, Type
from yakoon.engine.core.command import Command
from yakoon.engine.core.commandset import CommandSet
from yakoon.platform.commands.help.cmd_help import CmdHelpDomain


class MudHelpCommands(CommandSet):
    
    category = "help"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdHelpDomain,
        ]
