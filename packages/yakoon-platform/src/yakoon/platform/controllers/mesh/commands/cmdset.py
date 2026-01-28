from typing import Sequence, Type
from yakoon.base.commands.commandset import CommandSet
from yakoon.platform.commands.command import SaasCommand
from yakoon.platform.controllers.mesh.commands.cmd_dispatch import CmdDispatch


class MeshCommandSet(CommandSet):
    
    category = "system"

    @classmethod
    def commands(cls) -> Sequence[Type[SaasCommand]]: 
        return [
            CmdDispatch,
        ]