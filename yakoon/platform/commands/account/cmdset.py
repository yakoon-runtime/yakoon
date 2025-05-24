from typing import Sequence, Type
from yakoon.engine.core.command import Command
from yakoon.engine.core.commandset import CommandSet
from yakoon.platform.commands.account.cmd_login import CmdLogin
from yakoon.platform.settings import Settings


class PlatformAccountCommands(CommandSet):
    
    category = Settings.cmd_category_account

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdLogin,
        ]
