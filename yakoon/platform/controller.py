from yakoon.engine.core.domain.controller import BaseController
from yakoon.platform.commands.account.cmdset import PlatformAccountCommands
from yakoon.platform.commands.system.cmdset import PlatformSystemCommands
from yakoon.platform.runtime.session import PlatformSession
from yakoon.platform.services.session import SessionService


class PlatformController(BaseController):

    id: str = "platform"
    """Unique identifier used for command prefix resolution (e.g. realm:look, system:help)."""

    default_command_groups = ["system", "account"]     
    """ Defines the default command group. """

    commandsets = [
        PlatformSystemCommands, 
        PlatformAccountCommands]
    """ The collection of all commands. """
    
    async def on_platform_validate(self, session: PlatformSession):
        """
        Platform-level pre-send hook, called before request parsing.

        Used to prepare session context (e.g., account, locale, dynamic commands).
        Only invoked if this controller is the registered `system` controller.
        """
        registry = session.ctx._registry  # access intern by design

        # load the last controller
        controller = registry.get_controller_by_id(session.domain_id)
        session.domain = controller

        # builds the commandset for this session
        groups = set()
        for controller in registry.get_controllers():
            groups.update(controller.get_default_command_groups_with_prefix())
        session.cmd_groups = list(groups)
        def merge(lista: list[str], listb: list[str]) -> list[str]:
            return list(dict.fromkeys(lista + listb))

        # append the account commandset to this session
        if session.account:
            session.cmd_groups = merge(session.cmd_groups, session.account.cmd_groups)
        session.cmd_groups = sorted(session.cmd_groups)
            
    async def on_before_run_command(self, session: PlatformSession, request, command):
        """
        Hook called immediately before a single command is executed.
        Can be used to enforce permissions, inject context, or audit.
        """
        if required := getattr(command, "requires", []):
            if not set(required).issubset(set(session.permissions)):
                raise PermissionError(f"Auftrag abgelehnt! Erforderliche Rollen: {', '.join(required)}")

    async def on_platform_finalize(self, session: PlatformSession):
        """
        Platform-level post-send hook, called after command runing.

        Used to cleanup session context (e.g., account, locale, dynamic commands).
        Only invoked if this controller is the registered `system` controller.
        """
        await super().on_platform_finalize(session)
        if session.is_anonymous:
            await SessionService.delete_by_id(session.id)
