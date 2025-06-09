from typing import Sequence, Type
from yakoon.saas.commands.command import Command
from yakoon.saas.commands.commandset import CommandSet
from yakoon.saas.domains.realm.commands.account.general.cmd_ic import CmdIC
from yakoon.saas.controllers.gateway.settings import Settings


class GeneralAccountCommands(CommandSet):
    
    category = Settings.cmd_category_account

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdIC,
        ]
