from typing import Sequence, Type
from yakoon.saas.commands.command import SaasCommand
from yakoon.mesh.commands.commandset import CommandSet
from yakoon.saas.controllers.gateway.commands.account.cmd_login import CmdLogin
from yakoon.saas.settings import settings


class PlatformAccountCommands(CommandSet):
    
    category = settings.cmdsets.account

    @classmethod
    def commands(cls) -> Sequence[Type[SaasCommand]]: 
        return [
            CmdLogin,
        ]
