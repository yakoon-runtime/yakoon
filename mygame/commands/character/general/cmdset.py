from typing import Sequence, Type
from engine.core.command import Command
from engine.core.commandset import CommandSet
from mygame.commands.character.general.cmd_clock import CmdClock
from mygame.commands.character.general.cmd_detete import CmdDelete
from mygame.commands.character.general.cmd_look import CmdLook
from mygame.commands.character.general.cmd_move import CmdMove
from mygame.commands.character.general.cmd_teleport import CmdTeleport
from mygame.commands.character.general.cmd_ooc import CmdOOC


class GeneralCharacterCommands(CommandSet):
    
    mode = "character"

    @staticmethod
    def commands() -> Sequence[Type[Command]]: 
        return [
            CmdClock,
            CmdOOC,
            CmdTeleport,
            CmdLook,
            CmdDelete,
            CmdMove,
        ]