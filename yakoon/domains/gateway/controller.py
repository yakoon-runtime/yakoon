from yakoon.controllers.base import GatewayBaseController
from yakoon.domains.gateway.commands.account.cmdset import PlatformAccountCommands
from yakoon.domains.gateway.commands.system.cmdset import PlatformSystemCommands
from yakoon.domains.gateway.runtime.session import PlatformSession


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
    
    async def on_gateway_validate(self, session: PlatformSession):
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
        if session.account_id:
            account = await services.accounts.get_by_id(session.account_id)
            session.account = account
            session.cmd_groups = merge(session.cmd_groups, account.cmd_groups)
            
    async def on_before_run_command(self, session: PlatformSession, request, command):
        """
        Hook called immediately before a single command is executed.
        Can be used to enforce permissions, inject context, or audit.
        """
        if required := getattr(command, "requires", []):
            if not set(required).issubset(set(session.permissions)):
                raise PermissionError(f"Auftrag abgelehnt! Erforderliche Rollen: {', '.join(required)}")

    async def on_gateway_finalize(self, session: PlatformSession):
        """
        Platform-level post-send hook, called after command runing.

        Used to cleanup session context (e.g., account, locale, dynamic commands).
        Only invoked if this controller is the registered `gateway` controller.
        """
        await super().on_gateway_finalize(session)
        if session.is_anonymous:
            services = await self.service_router.get_registry(self.id)
            await services.sessions.delete_by_id(session.id)
