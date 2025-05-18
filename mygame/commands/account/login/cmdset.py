from typing import Sequence, Type
from engine.core.command import Command
from engine.core.commandset import CommandSet
from mygame.commands.account.login.cmd_login import CmdLogin


class LoginAccountCommands(CommandSet):
    
    mode = "login"

    @staticmethod
    def commands() -> Sequence[Type[Command]]: 
        return [
            CmdLogin,
        ]
