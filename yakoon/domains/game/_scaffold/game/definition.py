from yakoon.domains.game.controller import GameController as BaseDefinition

from .system.session import SolutionSession
from .commands.default_cmdsets import (
    PlatformAccountCommands,
    GeneralAccountCommands, 
    GeneralCharacterCommands, 
    )


class GameController(BaseDefinition):
    """
    Core configuration for the Smurf game.
    Connects session class and active command sets.
    """
    
    commandsets = [
        PlatformAccountCommands, 
        GeneralAccountCommands, 
        GeneralCharacterCommands
        # DebugCommands, AdminCommands, etc. later
    ]

    async def on_before_run_command(self, session: SolutionSession, request, command):
        # IMPORTANT: Call super() to retain base lifecycle behavior
        await super().on_before_run_command(session, request, command)

    async def on_after_run_command(self, session: SolutionSession, request, command):
        # IMPORTANT: Call super() to retain base lifecycle behavior
        await super().on_after_run_command(session, request, command)
