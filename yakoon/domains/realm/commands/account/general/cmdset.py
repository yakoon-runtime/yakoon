from typing import Sequence, Type
from yakoon.engine.core.command import Command
from yakoon.engine.core.commandset import CommandSet
from yakoon.domains.realm.commands.account.general.cmd_ic import CmdIC
from yakoon.platform.settings import Settings


class GeneralAccountCommands(CommandSet):
    
    category = Settings.cmd_category_account

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdIC,
        ]
