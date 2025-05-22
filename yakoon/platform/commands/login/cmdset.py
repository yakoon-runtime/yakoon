from typing import Sequence, Type
from yakoon.engine.core.command import Command
from yakoon.engine.core.commandset import CommandSet
from yakoon.platform.commands.login.cmd_login import CmdLogin


class LoginAccountCommands(CommandSet):
    
    mode = "login"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdLogin,
        ]
