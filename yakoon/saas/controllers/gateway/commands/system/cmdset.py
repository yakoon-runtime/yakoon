from typing import Sequence, Type
from yakoon.saas.commands.command import Command
from yakoon.saas.commands.commandset import CommandSet
from yakoon.saas.controllers.gateway.commands.system.cmd_switch import CmdSwitch
from yakoon.saas.controllers.gateway.commands.system.cmd_help import CmdHelpSystem
from yakoon.saas.controllers.gateway.commands.system.cmd_version import CmdVersion
from yakoon.saas.controllers.gateway.commands.system.cmd_welcome import CmdWelcome
from yakoon.saas.controllers.gateway.settings import Settings


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