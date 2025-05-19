from yakoon.game.definition import GameDefinition as BaseDefinition

from .system.session import GameSession
from .commands.default_cmdsets import (
    LoginAccountCommands,
    GeneralAccountCommands, 
    GeneralCharacterCommands, 
    )

class GameDefinition(BaseDefinition):
    session_cls = GameSession

    commandsets = [
        LoginAccountCommands, 
        GeneralAccountCommands, 
        GeneralCharacterCommands
    ]