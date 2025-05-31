from typing import Sequence, Type
from yakoon.core.command import Command
from yakoon.core.commandset import CommandSet
from yakoon.domains.platform.commands.account.cmd_login import CmdLogin
from yakoon.domains.platform.settings import Settings


class PlatformAccountCommands(CommandSet):
    
    category = Settings.cmd_category_account

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdLogin,
        ]
