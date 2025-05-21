from yakoon.domains.game.definition import GameDefinition as BaseDefinition

from .system.session import GameSession
from .commands.default_cmdsets import (
    LoginAccountCommands,
    GeneralAccountCommands, 
    GeneralCharacterCommands, 
    )


class GameDefinition(BaseDefinition):
    """
    Core configuration for the Smurf game.
    Connects session class and active command sets.
    """
    
    session_cls = GameSession

    commandsets = [
        LoginAccountCommands, 
        GeneralAccountCommands, 
        GeneralCharacterCommands
        # DebugCommands, AdminCommands, etc. later
    ]

    async def on_before_run_command(session: GameSession, request, command):
        # IMPORTANT: Call super() to retain base lifecycle behavior
        await super().on_before_run_command(session, request)

    async def on_after_run_command(session: GameSession, request, command):
        # IMPORTANT: Call super() to retain base lifecycle behavior
        await super().on_after_run_command(session, request)
