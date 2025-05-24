from typing import Sequence, Type
from yakoon.engine.core.command import Command
from yakoon.engine.core.commandset import CommandSet
from yakoon.platform.commands.system.cmd_create_domain_project import CmdCreateDomainProject
from yakoon.platform.commands.system.cmd_welcome import CmdWelcome


class PlatformSystemCommands(CommandSet):
    
    category = "system"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdWelcome,
            CmdCreateDomainProject,
        ]