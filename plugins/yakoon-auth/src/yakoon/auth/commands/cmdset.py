from typing import Sequence, Type
from yakoon.auth.commands.cmd_whoami import CmdWhoAmI
from yakoon.base.commands.command import Command
from yakoon.base.commands.commandset import CommandSet

from yakoon.auth.commands.cmd_su import CmdSu


class AuthSystemCommands(CommandSet):

    group = "system"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]:
        return [
            CmdSu,
            CmdWhoAmI,
        ]
