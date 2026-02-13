from typing import Sequence, Type
from yakoon.base.commands.command import Command
from yakoon.base.commands.commandset import CommandSet
from yakoon.office.mailing.commands.cmd_sendmail import CmdSendMail


class MailingCommands(CommandSet):

    group = "system"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]:
        return [
            CmdSendMail,
        ]
