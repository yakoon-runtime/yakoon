from typing import Sequence, Type
from yakoon.base.commands.command import Command
from yakoon.base.commands.commandset import CommandSet
from yakoon.shell.commands.shared.cmd_switch import CmdSwitch
from yakoon.shell.commands.shared.cmd_help import CmdHelpSystem
from yakoon.shell.commands.system.cmd_version import CmdVersion
from yakoon.shell.commands.system.cmd_welcome import CmdWelcome


class ShellSystemCommands(CommandSet):
    
    category = "system"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdVersion,
            CmdWelcome,
        ]