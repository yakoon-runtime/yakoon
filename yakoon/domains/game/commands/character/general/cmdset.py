from typing import Sequence, Type
from yakoon.engine.core.command import Command
from yakoon.engine.core.commandset import CommandSet
from yakoon.domains.game.commands.character.general.cmd_clock import CmdClock
from yakoon.domains.game.commands.character.general.cmd_detete import CmdDelete
from yakoon.domains.game.commands.character.general.cmd_look import CmdLook
from yakoon.domains.game.commands.character.general.cmd_move import CmdMove
from yakoon.domains.game.commands.character.general.cmd_teleport import CmdTeleport
from yakoon.domains.game.commands.character.general.cmd_ooc import CmdOOC


class GeneralCharacterCommands(CommandSet):
    
    category = "character"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdClock,
            CmdOOC,
            CmdTeleport,
            CmdLook,
            CmdDelete,
            CmdMove,
        ]