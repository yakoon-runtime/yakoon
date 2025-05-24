from typing import Sequence, Type
from yakoon.engine.core.command import Command
from yakoon.engine.core.commandset import CommandSet
from yakoon.platform.commands.system.cmd_help import CmdHelpDomain
from yakoon.platform.commands.system.cmd_switch import CmdSwitch
from yakoon.platform.settings import Settings


class PlatformSharedCommands(CommandSet):
    
    category = Settings.cmd_category_system

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdSwitch,
            CmdHelpDomain,
        ]