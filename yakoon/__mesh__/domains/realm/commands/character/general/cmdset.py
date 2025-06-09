from typing import Sequence, Type
from yakoon.saas.commands.command import Command
from yakoon.saas.commands.commandset import CommandSet
from yakoon.saas.domains.realm.commands.character.general.cmd_clock import CmdClock
from yakoon.saas.domains.realm.commands.character.general.cmd_look import CmdLook
from yakoon.saas.domains.realm.commands.character.general.cmd_move import CmdMove
from yakoon.saas.domains.realm.commands.character.general.cmd_teleport import CmdTeleport
from yakoon.saas.domains.realm.commands.character.general.cmd_ooc import CmdOOC


class GeneralCharacterCommands(CommandSet):
    
    category = "character"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [            
            CmdClock,
            CmdOOC,
            CmdTeleport,
            CmdLook,
            CmdMove,
        ]