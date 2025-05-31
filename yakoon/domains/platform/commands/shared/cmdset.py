from typing import Sequence, Type
from yakoon.core.command import Command
from yakoon.core.commandset import CommandSet
from yakoon.domains.platform.commands.system.cmd_help import CmdHelpDomain
from yakoon.domains.platform.commands.system.cmd_switch import CmdSwitch
from yakoon.domains.platform.settings import Settings


class PlatformSharedCommands(CommandSet):
    
    category = Settings.cmd_category_system

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdSwitch,
            CmdHelpDomain,
        ]