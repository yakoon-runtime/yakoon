from typing import Sequence, Type
from yakoon.saas.commands.command import Command
from yakoon.saas.commands.commandset import CommandSet
from yakoon.saas.controllers.gateway.commands.account.cmd_login import CmdLogin
from yakoon.saas.controllers.gateway.settings import Settings


class PlatformAccountCommands(CommandSet):
    
    category = Settings.cmd_category_account

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdLogin,
        ]
