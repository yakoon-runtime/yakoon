from yakoon.engine.core.domain.controller import BaseController
from yakoon.platform.commands.help.cmdset import PlatformHelpCommands
from yakoon.platform.commands.system.cmdset import PlatformSystemCommands
from yakoon.platform.commands.login.cmdset import LoginAccountCommands
from yakoon.platform.runtime.session import PlatformSession


class PlatformController(BaseController):

    name: str = "system"
    """Unique identifier used for command prefix resolution (e.g. mud:look, system:help)."""

    default_command_groups = ["help", "login"]     
    """ Defines the default command group. """

    commandsets = [
        PlatformHelpCommands,
        PlatformSystemCommands, 
        LoginAccountCommands]
    """ The collection of all commands. """
     
    async def on_before_send(self, session: PlatformSession):
        groups = set()
        registry = session.ctx._registry  # access intern by design

        for controller in registry.controllers + [registry.system]:
            groups.update(controller.get_default_command_groups_with_prefix())
        session.cmd_groups = list(groups)

        def merge(lista: list[str], listb: list[str]) -> list[str]:
            return list(dict.fromkeys(lista + listb))
        if session.account:
            session.cmd_groups = merge(session.cmd_groups, session.account.cmd_groups)
        session.cmd_groups = sorted(session.cmd_groups)
            
    async def on_before_run_command(self, session: PlatformSession, request, command):
        if required := getattr(command, "requires", []):
            if not set(required).issubset(set(session.permissions)):
                raise PermissionError(f"Auftrag abgelegt. Erforderliche Rollen: {', '.join(required)}")

    async def on_after_send(self, session: PlatformSession):
        await super().on_after_send(session)
        if session.is_anonymous:
            await session.ctx.sessions.delete(session.id)
