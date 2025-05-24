from typing import Sequence, Type
from yakoon.engine.core.command import Command
from yakoon.engine.core.commandset import CommandSet
from yakoon.platform.commands.system.cmd_switch import CmdSwitch
from yakoon.platform.commands.system.cmd_help import CmdHelpSystem
from yakoon.platform.commands.system.cmd_version import CmdVersion
from yakoon.platform.settings import Settings


class PlatformSystemCommands(CommandSet):
    
    category = Settings.cmd_category_system

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdVersion,
            CmdHelpSystem,
            CmdSwitch,
        ]