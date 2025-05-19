from typing import Sequence, Type
from yakoon.engine.core.command import Command
from yakoon.engine.core.commandset import CommandSet
from yakoon.game.commands.account.general.cmd_ic import CmdIC


class GeneralAccountCommands(CommandSet):
    
    mode = "account"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdIC,
        ]
