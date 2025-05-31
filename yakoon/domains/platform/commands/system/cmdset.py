from typing import Sequence, Type
from yakoon.core.command import Command
from yakoon.core.commandset import CommandSet
from yakoon.domains.platform.commands.system.cmd_switch import CmdSwitch
from yakoon.domains.platform.commands.system.cmd_help import CmdHelpSystem
from yakoon.domains.platform.commands.system.cmd_version import CmdVersion
from yakoon.domains.platform.commands.system.cmd_welcome import CmdWelcome
from yakoon.domains.platform.settings import Settings


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