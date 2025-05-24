from yakoon.engine.core.domain.controller import BaseController
from .commands.account.general.cmdset import GeneralAccountCommands
from .commands.help.cmdset import MudHelpCommands
from .commands.character.general.cmdset import GeneralCharacterCommands
from .runtime.clock import Clock
from .runtime.session import GameSession


class GameController(BaseController):

    name: str = "mud"
    """Unique identifier used for command prefix resolution (e.g. mud:look, system:help)."""

    clock = Clock()
    """ Defines the game clock. """

    session_cls = GameSession
    """ Defines the game session object. """

    default_command_groups = []     
    """ Defines the default command group. """

    commandsets = [
        MudHelpCommands,
        GeneralAccountCommands, 
        GeneralCharacterCommands]
    """ The collection of all commands. """
     
    async def on_before_run_command(self, session: GameSession, request, command):
        if required := getattr(command, "requires", []):
            if not set(required).issubset(set(session.permissions)):
                raise PermissionError(f"Du darfst das nicht tun. Erforderlich: {', '.join(required)}")
    
    async def on_after_run_command(self, session: GameSession, request, command):
        pass
        #if session.account and not session.character: 
        #     session.ctx.router.unregister(session.id)

    async def on_enter(self, session: GameSession):
        """
        Called after a user switches into this domain (e.g. via @switch).
        Used to show welcome messages, check account requirements, or guide login flow.
        Override this in each domain to define entry behavior.
        """
        await session.send_msg("Willkommen im MUD.")
        # if not session.account_id:
        #    await session.send_status("Melde dich mit `login <charakter>` an.")
