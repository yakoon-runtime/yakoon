from typing import Sequence, Type
from yakoon.mesh.commands.commandset import CommandSet
from yakoon.saas.commands.command import SaasCommand
from yakoon.saas.controllers.gateway.commands.system.cmd_switch import CmdSwitch
from yakoon.saas.controllers.gateway.commands.system.cmd_help import CmdHelpSystem
from yakoon.saas.controllers.gateway.commands.system.cmd_version import CmdVersion
from yakoon.saas.controllers.gateway.commands.system.cmd_welcome import CmdWelcome
from yakoon.saas.settings import settings


class PlatformSystemCommands(CommandSet):
    
    category = settings.cmdsets.system

    @classmethod
    def commands(cls) -> Sequence[Type[SaasCommand]]: 
        return [
            CmdVersion,
            CmdHelpSystem,
            CmdSwitch,
            CmdWelcome,
        ]