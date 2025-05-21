from yakoon.engine.core.domain.definition import DomainDefinition
from yakoon.platform.commands.system.cmdset import PlatformSystemCommands
from yakoon.platform.runtime.session import PlatformSession


class PlatformDefinition(DomainDefinition):

    session_cls = PlatformSession
    """ Defines the platform session object. """

    default_command_groups = ["system"]     
    """ Defines the default command group. """

    commandsets = [
        PlatformSystemCommands]
    """ The collection of all commands. """
     
    async def on_before_run_command(self, session: PlatformSession, request, command):
        if required := getattr(command, "requires", []):
            if not set(required).issubset(set(session.permissions)):
                raise PermissionError(f"Auftrag abgelegt. Erforderliche Rollen: {', '.join(required)}")

    async def on_after_run_command(self, session, request, command):
        # IMPORTANT: Call super() to retain base lifecycle behavior
        await super().on_after_run_command(session, request, command)
