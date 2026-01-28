from typing import Sequence, Type
from yakoon.platform.commands.command import SaasCommand
from yakoon.base.commands.commandset import CommandSet
from yakoon.platform.controllers.gateway.commands.system.cmd_help import CmdHelpDomain
from yakoon.platform.controllers.gateway.commands.system.cmd_switch import CmdSwitch
from yakoon.platform.settings import settings


class PlatformSharedCommands(CommandSet):
    
    category = settings.cmdsets.system

    @classmethod
    def commands(cls) -> Sequence[Type[SaasCommand]]: 
        return [
            CmdSwitch,
            CmdHelpDomain,
        ]