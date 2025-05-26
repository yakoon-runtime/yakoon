from yakoon.domains.game.runtime.data import RuntimeGameData
from yakoon.domains.game.stores.character_store import CharacterStore
from yakoon.engine.core.domain.controller import BaseController
from yakoon.platform.commands.shared.cmdset import PlatformSharedCommands
from yakoon.solution.platform.runtime.session import SolutionSession
from .commands.account.general.cmdset import GeneralAccountCommands
from .commands.character.general.cmdset import GeneralCharacterCommands
from .runtime.clock import Clock

class GameController(BaseController):

    name: str = "mud"
    """Unique identifier used for command prefix resolution (e.g. mud:look, system:help)."""

    clock = Clock()
    """ Defines the game clock. """

    default_command_groups = []     
    """ Defines the default command group. """

    commandsets = [
        PlatformSharedCommands,
        GeneralAccountCommands, 
        GeneralCharacterCommands]
    """ The collection of all commands. """
     
    async def on_before_send(self, session: SolutionSession):
        """
        Prepares the session's runtime state before any command is executed within this domain.

        Typically used to:
        - Load domain-specific objects (e.g., Character) into session.data_runtime
        - Ensure the session is ready for domain-specific command execution

        This method is called once per command dispatch cycle.
        """
        session.data_runtime = RuntimeGameData(None)
        char_id = session.data_storage.get(self.name, "char_id")
        if char_id:
            character = CharacterStore.get_by_id(char_id)
            session.data_runtime = RuntimeGameData(character)
 
    async def on_before_run_command(self, session: SolutionSession, request, command):
        if required := getattr(command, "requires", []):
            if not set(required).issubset(set(session.permissions)):
                raise PermissionError(f"Du darfst das nicht tun. Erforderlich: {', '.join(required)}")
    
    async def on_after_run_command(self, session: SolutionSession, request, command):
        pass
        #if session.account and not session.character: 
        #     session.ctx.router.unregister(session.id)

    async def on_enter(self, session: SolutionSession):
        """
        Called after a user switches into this domain (e.g. via @switch).
        Used to show welcome messages, check account requirements, or guide login flow.
        Override this in each domain to define entry behavior.
        """
        await session.send_msg("Willkommen im MUD.")
        # if not session.account_id:
        #    await session.send_status("Melde dich mit `login <charakter>` an.")
