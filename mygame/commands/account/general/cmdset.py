from typing import Sequence, Type
from engine.core.command import Command
from engine.core.commandset import CommandSet
from mygame.commands.account.general.cmd_ic import CmdIC


class GeneralAccountCommands(CommandSet):
    
    mode = "account"

    @staticmethod
    def commands() -> Sequence[Type[Command]]: 
        return [
            CmdIC,
        ]
