from __future__ import annotations
from typing import TYPE_CHECKING, Sequence, Type

from yakoon.base.controllers.base import BaseController
from yakoon.base.descriptors.workflow import WorkflowSource
from yakoon.base.descriptors.template import TemplateSource

from yakoon.shell.commands.system.cmdset import ShellSystemCommands
from yakoon.shell.commands.workflow.cmdset import ShellWorkflowCommands


if TYPE_CHECKING:
    from yakoon.base.commands.request import Request
    from yakoon.base.runtime.session import Session
    from yakoon.base.commands.command import Command
    from yakoon.base.commands.commandset import CommandSet


class ShellCoreController(BaseController):
    """Core shell controller.

    This controller provides the default interactive shell environment:
      - system commands (help/man/exit, etc.)
      - workflow commands (wf.*)
      - templates and workflows rooted in yakoon.shell:core
    """

    id: str = "shell"
    is_shell: bool = True
    is_listed: bool = True
    is_activatable: bool = True

    # Framework-scharf: builtins als Mapping (Key -> Command-Key).
    # Damit kannst du später Alias/Mapping sauber erweitern, ohne Set-Magie.
    shell_builtins: dict[str, str] = {
        "exit": "exit",
        "man": "man",
        "wf.run": "wf.run",
        "wf.prompt": "wf.prompt",
        "wf.next": "wf.next",
        "wf.cancel": "wf.cancel", 
    }

    template_source = TemplateSource(
        package="yakoon.shell",
        template_sub_path="core",
    )

    workflow_source = WorkflowSource(
        package="yakoon.shell",
        workflow_sub_path="core",
    )

    @property
    def commandsets(self) -> Sequence[Type[CommandSet]]:
        """Command sets exported by the shell controller."""
        return (ShellSystemCommands, ShellWorkflowCommands)

    async def on_before_run_command(self, session: Session, request: Request, command: Command) -> None:
        """Touch session before executing any command.

        Notes:
            Keeping this in the controller makes the behavior consistent across all
            shell commands (system and workflow), without duplicating it in each command.
        """
        session.touch()
