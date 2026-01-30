from typing import Sequence, Type
from yakoon.base.commands.command import Command
from yakoon.base.commands.commandset import CommandSet
from yakoon.shell.commands.shared.cmd_help import CmdHelpDomain
from yakoon.shell.commands.shared.cmd_switch import CmdSwitch


class ShellSharedCommands(CommandSet):
    
    category = "system"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdSwitch,
            CmdHelpDomain,
        ]