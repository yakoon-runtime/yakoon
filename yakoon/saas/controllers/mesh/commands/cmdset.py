from typing import Sequence, Type
from yakoon.mesh.commands.commandset import CommandSet
from yakoon.saas.commands.command import SaasCommand
from yakoon.saas.controllers.mesh.commands.cmd_dispatch import CmdDispatch


class MeshCommandSet(CommandSet):
    
    category = "system"

    @classmethod
    def commands(cls) -> Sequence[Type[SaasCommand]]: 
        return [
            CmdDispatch,
        ]