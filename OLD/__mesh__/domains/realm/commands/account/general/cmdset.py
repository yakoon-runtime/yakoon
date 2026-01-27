from typing import Sequence, Type
from yakoon.platform.commands.command import SaasCommand
from yakoon.base.commands.commandset import CommandSet
from yakoon.platform.domains.realm.commands.account.general.cmd_ic import CmdIC
from yakoon.platform.settings import settings


class GeneralAccountCommands(CommandSet):
    
    category = settings.cmdsets.account

    @classmethod
    def commands(cls) -> Sequence[Type[SaasCommand]]: 
        return [
            CmdIC,
        ]
