from yakoon.controllers.base import GatewayBaseController
from yakoon.domains.gateway.commands.account.cmdset import PlatformAccountCommands
from yakoon.domains.gateway.commands.system.cmdset import PlatformSystemCommands
from yakoon.models.key import Key
from yakoon.models.namespace import Namespace
from yakoon.runtime.models.session import BaseSession
from yakoon.domains.gateway.setup import setup_gateway


class GatewayController(GatewayBaseController):

    id: str = "gateway"
    """Unique identifier used for command prefix resolution (e.g. realm:look, system:help)."""

    default_command_groups = ["system", "account"]     
    """Names of command groups that are automatically active for every session, 
    without requiring explicit permissions."""

    commandsets = [
        PlatformSystemCommands, 
        PlatformAccountCommands]
    """ The collection of all commands. """
    
    def __init__(self):
        super().__init__()    
        setup_gateway(self.service_router, self.id)

    async def on_resolve_session(self, session_key: Key) -> BaseSession:
        """
        Resolves the session object for the given request.

        This method decides whether to load an existing session from storage,
        create a new transient session, or reject the request entirely.

        It must not persist the session unless a valid context (e.g. login) has been established.
        The returned session should be usable by the engine but may remain in-memory only.

        Returns:
            BaseSession: a session instance bound to the request lifecycle
        """
        ns = Namespace(domain="yakoon", bucket="bucket", scope="develop")
        session_key = session_key or ns.get_key(None)
        services = await self.get_system_services()        

        session = await services.sessions.get_or_new(session_key)        
        session.touch() # Updates the last activity.
        
        return session

    async def on_gateway_validate(self, session: BaseSession):
        """
        Platform-level pre-send hook, called before request parsing.

        Used to prepare session context (e.g., account, locale, dynamic commands).
        Only invoked if this controller is the registered `system` controller.
        """
        services = await self.get_gateway_services()

        # builds the commandset for this session
        groups = set()
        registry = await self.get_controller_registry()
        for controller in registry.get_controllers():
            groups.update(controller.get_default_command_groups_with_prefix())
        session.cmd_groups = list(groups)

        def merge(lista: list[str], listb: list[str]) -> list[str]:
            return sorted(list(dict.fromkeys(lista + listb)))
        
        # Middleware-Hook: Session was loaded, Account is missing?
        account_key = session.ctx("gateway", "account_key", persist=True)
        if account_key:
            account = await services.accounts.get_by_key(account_key)
            session.set_ctx("gateway", "account", account, persist=False)
            session.cmd_groups = merge(session.cmd_groups, account.cmd_groups)
            
    async def on_before_run_command(self, session: BaseSession, request, command):
        """
        Hook called immediately before a single command is executed.
        Can be used to enforce permissions, inject context, or audit.
        """
        if required := getattr(command, "requires", []):
            if not set(required).issubset(set(session.permissions)):
                raise PermissionError(f"Auftrag abgelehnt! Erforderliche Rollen: {', '.join(required)}")

    async def on_gateway_finalize(self, session: BaseSession):
        """
        Platform-level post-send hook, called after command runing.

        Used to cleanup session context (e.g., account, locale, dynamic commands).
        Only invoked if this controller is the registered `gateway` controller.
        """
        await super().on_gateway_finalize(session)
        if not session.ctx("gateway", "account_key", persist=True):
            services = await self.get_system_services()
            await services.sessions.delete_by_key(session.key)
