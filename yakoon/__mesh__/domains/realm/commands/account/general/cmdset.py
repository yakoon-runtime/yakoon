from typing import Sequence, Type
from yakoon.saas.commands.command import SaasCommand
from yakoon.mesh.commands.commandset import CommandSet
from yakoon.saas.domains.realm.commands.account.general.cmd_ic import CmdIC
from yakoon.saas.settings import settings


class GeneralAccountCommands(CommandSet):
    
    category = settings.cmdsets.account

    @classmethod
    def commands(cls) -> Sequence[Type[SaasCommand]]: 
        return [
            CmdIC,
        ]
