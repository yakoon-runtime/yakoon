from typing import Sequence, Type
from yakoon.commands.command import Command
from yakoon.commands.commandset import CommandSet
from yakoon.domains.realm.commands.account.general.cmd_ic import CmdIC
from yakoon.domains.gateway.settings import Settings


class GeneralAccountCommands(CommandSet):
    
    category = Settings.cmd_category_account

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdIC,
        ]
