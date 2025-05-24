from typing import Sequence, Type
from yakoon.engine.core.command import Command
from yakoon.engine.core.commandset import CommandSet
from yakoon.platform.commands.login.cmd_login import CmdLogin
from yakoon.platform.commands.login.cmd_switch import CmdSwitch


class LoginAccountCommands(CommandSet):
    
    category = "login"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdLogin,
            CmdSwitch,
        ]
