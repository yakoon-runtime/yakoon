from yakoon.domains.realm.commands.account.general.cmdset import GeneralAccountCommands
from yakoon.domains.realm.commands.character.general.cmdset import GeneralCharacterCommands
from yakoon.domains.realm.runtime.clock import Clock
from yakoon.domains.realm.runtime.data import RuntimeRealmData
from yakoon.domains.realm.runtime.direction import get_exit_direction_commandset
from yakoon.domains.realm.services.bindings.memory import bind_memory_services
from yakoon.controllers.base.gateway import BaseController
from yakoon.domains.gateway.commands.shared.cmdset import PlatformSharedCommands
from yakoon.domains.gateway.runtime.session import GatewaySession
from yakoon.runtime.system.router import ServiceRouter


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
     
    def __init__(self):
        super().__init__()    
        self.service_router = ServiceRouter()
        self.service_router.register_static(self.id, bind_memory_services())

    def dynamic_prefix(self, session: GatewaySession) -> str:
        """
        Returns the command group prefix for dynamic, session-local commands.
        """
        return f"{self.id}:dynamic:{session.id}"

    async def on_before_resolve(self, session: GatewaySession):
        """
        Hook called before command resolution.

        Use this to register dynamic commands for the current session,
        e.g. exits, room-specific actions or context-sensitive shortcuts.
        Executed regardless of whether a valid command is found.
        """
        session.data_runtime = RuntimeRealmData(None)
        char_id = session.data_storage.get(self.id, "char_id")
        if not char_id:
            return
        
        services = await self.get_domain_services()
        ns = await services.namespaces.from_session(session)

        character = await services.chars.get_by_id(ns, char_id)
        if not character:
            return
        
        room = await services.rooms.get_by_id(ns, character.location)
        if not room:
            return

        dynamic = self.dynamic_prefix(session)
        session.cmd_groups_dynamic = [dynamic]

        self.router.unregister(dynamic)
        self.router.register(dynamic, get_exit_direction_commandset(room))
  
    async def on_before_run_command(self, session: GatewaySession, request, command):
        char_id = session.data_storage.get(self.id, "char_id")
        services = await self.get_domain_services()
        ns = await services.namespaces.from_session(session)

        if char_id:           
            character = await services.chars.get_by_id(ns, char_id)
            session.data_runtime = RuntimeRealmData(character)  

        if required := getattr(command, "requires", []):
            if not set(required).issubset(set(session.permissions)):
                raise PermissionError(f"Du darfst das nicht tun. Erforderlich: {', '.join(required)}")

        # default: character is required
        if getattr(command, "requires_character", False):            
            if not session.data_runtime or not session.data_runtime.character:
                raise PermissionError("Du brauchst dazu einen Spieler: Verwende 'ic <character>'.")

    async def on_enter(self, session: GatewaySession):
        """
        Called after a user switches into this domain (e.g. via @switch).
        Used to show welcome messages, check account requirements, or guide login flow.
        Override this in each domain to define entry behavior.
        """
        await session.emit("Willkommen im MUD.")
        await session.notify("Melde dich mit `ic <charakter>` an.")        

    async def on_cleanup(self, session: GatewaySession):
        """
        Always called after a command cycle, even if exceptions occurred.

        Use this to remove dynamic command groups, reset state,
        or undo temporary session changes.
        """        
        self.router.unregister(self.dynamic_prefix(session))
