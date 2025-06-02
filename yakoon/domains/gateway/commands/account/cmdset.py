from typing import Sequence, Type
from yakoon.commands.command import Command
from yakoon.commands.commandset import CommandSet
from yakoon.domains.gateway.commands.account.cmd_login import CmdLogin
from yakoon.domains.gateway.settings import Settings


class PlatformAccountCommands(CommandSet):
    
    category = Settings.cmd_category_account

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdLogin,
        ]
