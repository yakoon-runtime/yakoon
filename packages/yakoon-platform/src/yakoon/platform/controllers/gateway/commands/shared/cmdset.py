from typing import Sequence, Type
from yakoon.base.commands.command import Command
from yakoon.base.commands.commandset import CommandSet
from yakoon.platform.controllers.gateway.commands.system.cmd_help import CmdHelpDomain
from yakoon.platform.controllers.gateway.commands.system.cmd_switch import CmdSwitch
from yakoon.platform.settings import settings


class PlatformSharedCommands(CommandSet):
    
    category = settings.cmdsets.system

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdSwitch,
            CmdHelpDomain,
        ]