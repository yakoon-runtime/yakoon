from yakoon.base.controllers.base import BaseController
from yakoon.base.models.key import Key
from yakoon.base.ports import SessionService
from yakoon.base.descriptors.template import TemplateSource
from yakoon.base.runtime.session import Session

from yakoon.shell.commands.system.cmdset import ShellSystemCommands


class ShellCoreController(BaseController):

    id: str = "shell"
    """Unique identifier used for command prefix resolution (e.g. realm:look, system:help)."""

    is_shell: bool = True
    is_listed: bool = True
    is_activatable: bool = True

    shell_builtins = {"exit", "man"}

    default_command_groups = ["system", "account"]     
    """Names of command groups that are automatically active for every session, 
    without requiring explicit permissions."""

    template_source = TemplateSource(
        package="yakoon.shell",
        sub_template_path="core")

    commandsets = [
        ShellSystemCommands]
    """ The collection of all commands. """
                    
    async def on_before_run_command(self, session: Session, request, command):
        """
        Hook called immediately before a single command is executed.
        Can be used to enforce permissions, inject context, or audit.
        """
        session.touch()

