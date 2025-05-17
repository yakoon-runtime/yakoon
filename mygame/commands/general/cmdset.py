from typing import Sequence, Type
from engine.core.command import Command
from engine.core.commandset import CommandSet
from mygame.commands.general.cmd_detete import CmdDelete
from mygame.commands.general.cmd_look import CmdLook
from mygame.commands.general.cmd_move import CmdMove
from mygame.commands.general.cmd_teleport import CmdTeleport


class GeneralCommands(CommandSet):
    
    @staticmethod
    def commands() -> Sequence[Type[Command]]: 
        return [
            CmdTeleport,
            CmdLook,
            CmdDelete,
            CmdMove,
        ]