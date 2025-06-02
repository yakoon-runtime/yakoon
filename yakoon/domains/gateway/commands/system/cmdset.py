from typing import Sequence, Type
from yakoon.commands.command import Command
from yakoon.commands.commandset import CommandSet
from yakoon.domains.gateway.commands.system.cmd_switch import CmdSwitch
from yakoon.domains.gateway.commands.system.cmd_help import CmdHelpSystem
from yakoon.domains.gateway.commands.system.cmd_version import CmdVersion
from yakoon.domains.gateway.commands.system.cmd_welcome import CmdWelcome
from yakoon.domains.gateway.settings import Settings


class PlatformSystemCommands(CommandSet):
    
    category = Settings.cmd_category_system

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdVersion,
            CmdHelpSystem,
            CmdSwitch,
            CmdWelcome,
        ]