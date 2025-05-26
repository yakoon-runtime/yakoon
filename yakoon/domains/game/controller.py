from yakoon.domains.game.runtime.data import RuntimeGameData
from yakoon.domains.game.runtime.direction import get_exit_direction_commandset
from yakoon.domains.game.stores.character_store import CharacterStore
from yakoon.domains.game.stores.room_store import RoomStore
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
     
    def dynamic_prefix(self, session: SolutionSession) -> str:
        """
        Returns the command group prefix for dynamic, session-local commands.
        """
        return f"mud:dynamic:{session.id}"

    async def on_before_resolve(self, session: SolutionSession):
        """
        Hook called before command resolution.

        Use this to register dynamic commands for the current session,
        e.g. exits, room-specific actions or context-sensitive shortcuts.
        Executed regardless of whether a valid command is found.
        """
        session.data_runtime = RuntimeGameData(None)
        char_id = session.data_storage.get(self.name, "char_id")
        if not char_id:
            return
        character = CharacterStore.get_by_id(char_id)
        if not character:
            return
        room = RoomStore.get_by_id(character.location)
        if not room:
            return

        dynamic = self.dynamic_prefix(session)
        session.cmd_groups_dynamic = [dynamic]

        self.router.unregister(dynamic)
        self.router.register(dynamic, get_exit_direction_commandset(room))

    async def on_before_send(self, session: SolutionSession):
        """
        Prepares the session's runtime state before any command is executed within this domain.

        Typically used to:
        - Load domain-specific objects (e.g., Character) into session.data_runtime
        - Ensure the session is ready for domain-specific command execution

        This method is called once per command dispatch cycle.
        """        
        char_id = session.data_storage.get(self.name, "char_id")
        if not char_id:
            return

        character = CharacterStore.get_by_id(char_id)
        session.data_runtime = RuntimeGameData(character)  

    async def on_before_run_command(self, session: SolutionSession, request, command):
        if required := getattr(command, "requires", []):
            if not set(required).issubset(set(session.permissions)):
                raise PermissionError(f"Du darfst das nicht tun. Erforderlich: {', '.join(required)}")

        # default: character is required
        if getattr(command, "requires_character", True):            
            if not session.data_runtime or not session.data_runtime.character:
                raise PermissionError("Du brauchst dazu einen Spieler: Verwende 'ic <character>'.")

    async def on_enter(self, session: SolutionSession):
        """
        Called after a user switches into this domain (e.g. via @switch).
        Used to show welcome messages, check account requirements, or guide login flow.
        Override this in each domain to define entry behavior.
        """
        await session.send_msg("Willkommen im MUD.")
        await session.send_status("Melde dich mit `ic <charakter>` an.")        

    async def on_cleanup(self, session: SolutionSession):
        """
        Always called after a command cycle, even if exceptions occurred.

        Use this to remove dynamic command groups, reset state,
        or undo temporary session changes.
        """        
        self.router.unregister(self.dynamic_prefix(session))
