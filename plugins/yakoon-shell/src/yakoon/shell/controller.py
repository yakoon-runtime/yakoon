from yakoon.base.controllers.base import BaseController
from yakoon.base.descriptors.workflow import WorkflowSource
from yakoon.base.descriptors.template import TemplateSource
from yakoon.base.runtime.session import Session

from yakoon.shell.commands.system.cmdset import ShellSystemCommands
from yakoon.shell.commands.workflow.cmdset import ShellWorkflowCommands


class ShellCoreController(BaseController):

    id: str = "shell"
    """Unique identifier used for command prefix resolution (e.g. realm:look, system:help)."""

    is_shell: bool = True
    is_listed: bool = True
    is_activatable: bool = True

    shell_builtins = {
        "exit", "man", 
        "wf.run", "wf.prompt", "wf.next", "wf.cancel"}

    template_source = TemplateSource(
        package="yakoon.shell",
        template_sub_path="core")

    workflow_source = WorkflowSource(
        package="yakoon.shell",
        workflow_sub_path="core")

    commandsets = [
        ShellSystemCommands, 
        ShellWorkflowCommands]
    """ The collection of all commands. """
                    
    async def on_before_run_command(self, session: Session, request, command):
        """
        Hook called immediately before a single command is executed.
        Can be used to enforce permissions, inject context, or audit.
        """
        session.touch()

