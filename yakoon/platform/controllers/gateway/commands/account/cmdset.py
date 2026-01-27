from typing import Sequence, Type
from yakoon.platform.commands.command import SaasCommand
from yakoon.base.commands.commandset import CommandSet
from yakoon.platform.controllers.gateway.commands.account.cmd_login import CmdLogin
from yakoon.platform.settings import settings


class PlatformAccountCommands(CommandSet):
    
    category = settings.cmdsets.account

    @classmethod
    def commands(cls) -> Sequence[Type[SaasCommand]]: 
        return [
            CmdLogin,
        ]
