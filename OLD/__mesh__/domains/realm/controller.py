from yakoon.platform.domains.realm.commands.account.general.cmdset import GeneralAccountCommands
from yakoon.platform.domains.realm.commands.character.general.cmdset import GeneralCharacterCommands
from yakoon.platform.domains.realm.runtime.clock import Clock
from yakoon.platform.domains.realm.runtime.direction import get_exit_direction_commandset
from yakoon.platform.controllers.base.gateway import BaseController
from yakoon.platform.controllers.gateway.commands.shared.cmdset import PlatformSharedCommands
from yakoon.base.runtime.session import BaseSession
from yakoon.platform.domains.realm.setup import setup_realm


class RealmController(BaseController):

    id: str = "realm"
    """Unique identifier used for command prefix resolution (e.g. realm:look, system:help)."""

    clock = Clock()
    """ Defines the realm clock. """

    default_command_groups = []     
    """Names of command groups that are automatically active for every session, 
    without requiring explicit permissions."""

    commandsets = [
        #. TODO: braucht es das? fallen commands nicht ohnehin durch?
        PlatformSharedCommands, 
        GeneralAccountCommands, 
        GeneralCharacterCommands]
    """The collection of all commands."""
     
    async def on_initialize(self, session: BaseSession):
        """
        Called after the controller has been fully constructed but before any commands are processed.

        Use this hook to perform asynchronous setup tasks such as loading data, initializing services,
        or validating infrastructure state (e.g., ensuring the admin account exists).

        This method is guaranteed to run once before the first engine tick or command dispatch.
        """
        await setup_realm(self.service_router, "realm")

    def dynamic_prefix(self, session: BaseSession) -> str:
        """
        Returns the command group prefix for dynamic, session-local commands.
        """
        return f"{self.id}:dynamic:{session.key}"

    async def on_before_resolve(self, session: BaseSession):
        """
        Hook called before command resolution.

        Use this to register dynamic commands for the current session,
        e.g. exits, room-specific actions or context-sensitive shortcuts.
        Executed regardless of whether a valid command is found.
        """        
        char_key = session.ctx("realm", "char_key", persist=True)
        if not char_key:
            return
        
        services = await self.get_domain_services()
        ns = await self.get_namespace(session)

        character = await services.chars.get_by_key(char_key)
        if not character:
            return
        
        room = await services.rooms.get_by_id(ns, character.location)
        if not room:
            return

        dynamic = self.dynamic_prefix(session)
        session.cmd_groups_dynamic = [dynamic]

        self.router.unregister(dynamic)
        self.router.register(dynamic, get_exit_direction_commandset(room))
  
    async def on_before_run_command(self, session: BaseSession, request, command):
        services = await self.get_domain_services()
        ns = await self.get_namespace(session)

        char_key = session.ctx("realm", "char_key", persist=True)
        if char_key:           
            character = await services.chars.get_by_key(char_key)
            session.set_ctx("realm", "char", character, persist=False)  

        if required := getattr(command, "requires", []):
            account = session.ctx("gateway", "account", persist=False)
            if not account or not set(required).issubset(set(account.permissions)):
                raise PermissionError(f"Du darfst das nicht tun. Erforderlich: {', '.join(required)}")

        # default: character is required
        if getattr(command, "requires_character", False):            
            if not session.ctx("realm", "char", persist=False):
                raise PermissionError("Du brauchst dazu einen Spieler: Verwende 'ic <character>'.")

    async def on_enter(self, session: BaseSession):
        """
        Called after a user switches into this domain (e.g. via @switch).
        Used to show welcome messages, check account requirements, or guide login flow.
        Override this in each domain to define entry behavior.
        """
        await session.emit("Willkommen im MUD.")
        await session.notify("Melde dich mit `ic <charakter>` an.")        

    async def on_cleanup(self, session: BaseSession):
        """
        Always called after a command cycle, even if exceptions occurred.

        Use this to remove dynamic command groups, reset state,
        or undo temporary session changes.
        """        
        self.router.unregister(self.dynamic_prefix(session))
