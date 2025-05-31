from typing import Sequence, Type
from yakoon.core.command import Command
from yakoon.core.commandset import CommandSet
from yakoon.domains.realm.commands.account.general.cmd_ic import CmdIC
from yakoon.domains.platform.settings import Settings


class GeneralAccountCommands(CommandSet):
    
    category = Settings.cmd_category_account

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdIC,
        ]
