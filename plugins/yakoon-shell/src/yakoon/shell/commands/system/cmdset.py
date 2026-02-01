from typing import Sequence, Type
from yakoon.base.commands.command import Command
from yakoon.base.commands.commandset import CommandSet
from yakoon.shell.commands.system.cmd_exit import CmdExit
from yakoon.shell.commands.system.cmd_man import CmdMan
from yakoon.shell.commands.system.cmd_use import CmdUse
from yakoon.shell.commands.system.cmd_version import CmdVersion
from yakoon.shell.commands.system.cmd_welcome import CmdWelcome


class ShellSystemCommands(CommandSet):
    
    category = "system"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdWelcome,
            CmdVersion,
            CmdUse,
            CmdExit,
            CmdMan,
        ]