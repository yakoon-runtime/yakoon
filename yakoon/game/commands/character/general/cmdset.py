from typing import Sequence, Type
from yakoon.engine.core.command import Command
from yakoon.engine.core.commandset import CommandSet
from yakoon.game.commands.character.general.cmd_clock import CmdClock
from yakoon.game.commands.character.general.cmd_detete import CmdDelete
from yakoon.game.commands.character.general.cmd_look import CmdLook
from yakoon.game.commands.character.general.cmd_move import CmdMove
from yakoon.game.commands.character.general.cmd_teleport import CmdTeleport
from yakoon.game.commands.character.general.cmd_ooc import CmdOOC


class GeneralCharacterCommands(CommandSet):
    
    mode = "character"

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