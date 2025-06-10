from typing import Sequence, Type
from yakoon.saas.commands.command import SaasCommand
from yakoon.mesh.commands.commandset import CommandSet
from yakoon.saas.controllers.gateway.commands.system.cmd_help import CmdHelpDomain
from yakoon.saas.controllers.gateway.commands.system.cmd_switch import CmdSwitch
from yakoon.saas.settings import settings


class PlatformSharedCommands(CommandSet):
    
    category = settings.cmdsets.system

    @classmethod
    def commands(cls) -> Sequence[Type[SaasCommand]]: 
        return [
            CmdSwitch,
            CmdHelpDomain,
        ]