from yakoon.engine.core.domain.controller import BaseController
from yakoon.engine.system.session import BaseSession
from yakoon.platform.commands.system.cmdset import PlatformSystemCommands
from yakoon.platform.commands.login.cmdset import LoginAccountCommands
from yakoon.platform.runtime.session import PlatformSession
from yakoon.platform.services.session_service import SessionService
from yakoon.platform.stores.memory_session_store import InMemorySessionStore


class PlatformController(BaseController):

    name: str = "system"
    """Unique identifier used for command prefix resolution (e.g. mud:look, system:help)."""

    default_command_groups = ["login"]     
    """ Defines the default command group. """

    commandsets = [
        PlatformSystemCommands, 
        LoginAccountCommands]
    """ The collection of all commands. """
     
    async def on_before_run_command(self, session: PlatformSession, request, command):
        if required := getattr(command, "requires", []):
            if not set(required).issubset(set(session.permissions)):
                raise PermissionError(f"Auftrag abgelegt. Erforderliche Rollen: {', '.join(required)}")

    async def on_after_send(self, session: PlatformSession):
        await super().on_after_send(session)
        if session.is_anonymous:
            await session.ctx.sessions.delete(session.id)
