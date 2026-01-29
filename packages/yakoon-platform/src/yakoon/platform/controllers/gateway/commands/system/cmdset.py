from typing import Sequence, Type
from yakoon.base.commands.command import MeshCommand
from yakoon.base.commands.commandset import CommandSet
from yakoon.platform.controllers.gateway.commands.system.cmd_switch import CmdSwitch
from yakoon.platform.controllers.gateway.commands.system.cmd_help import CmdHelpSystem
from yakoon.platform.controllers.gateway.commands.system.cmd_version import CmdVersion
from yakoon.platform.controllers.gateway.commands.system.cmd_welcome import CmdWelcome
from yakoon.platform.settings import settings


class PlatformSystemCommands(CommandSet):
    
    category = settings.cmdsets.system

    @classmethod
    def commands(cls) -> Sequence[Type[MeshCommand]]: 
        return [
            CmdVersion,
            CmdHelpSystem,
            CmdSwitch,
            CmdWelcome,
        ]