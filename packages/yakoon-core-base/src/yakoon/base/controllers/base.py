from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence, Type, TYPE_CHECKING

from yakoon.base.commands.commandset import CommandSet
from yakoon.base.commands.request import Request
from yakoon.base.descriptors.workflow import WorkflowSource
from yakoon.base.ports import NamespaceService
from yakoon.base.directories.service import ServiceDirectory
from yakoon.base.descriptors.template import TemplateSource

if TYPE_CHECKING:
    from yakoon.base.commands.command import Command
    from yakoon.base.models.ns import Namespace
    from yakoon.base.runtime.session import Session


class BaseController(ABC):
    """Abstract base class for controllers.

    A controller is the composition root for a "program context" in the engine:
      - it provides services via a ServiceDirectory
      - it defines available commands via CommandSets
      - it provides template and workflow sources
      - it exposes lifecycle hooks around resolution and execution

    Public API contract:
      - `commandsets` is the authoritative way to expose commands for registration.
      - `services` is injected at runtime (platform responsibility).
      - Hooks must be side-effect safe and should not assume a command exists unless
        their signature includes one.

    Notes:
        Keep controllers lightweight. Business logic belongs in services and commands.
    """

    id: str = "unnamed"
    """Unique controller identifier used for command prefix resolution."""

    is_shell: bool = False
    """If True, the controller acts as a shell-like environment."""

    is_listed: bool = True
    """If False, the controller is hidden from listings (e.g. man/help, UI menus)."""

    is_activatable: bool = True
    """If False, the controller cannot be activated as an interactive context."""

    shell_builtins: dict[str, Type["Command"]] = {}
    """Commands available regardless of active controller context.

    Warning:
        Avoid mutating this mapping at runtime for public-framework stability.
        If you need dynamic builtins, provide them via `on_before_resolve`.
    """

    template_source: TemplateSource = TemplateSource(None)
    """Template source used by presenters for command output and man pages.

    Template selection should be based on conventions (e.g. `cmd_*`, `man_*`),
    not hard-coded paths in commands.
    """

    workflow_source: WorkflowSource = WorkflowSource(None)
    """Workflow source providing workflow definitions owned by this controller."""

    def __init__(self) -> None:
        """Initialize a controller with an empty service directory.

        The platform is expected to inject a fully configured directory via
        `connect_services()` before command execution.
        """
        self.services: ServiceDirectory = ServiceDirectory()
        """Bucket-based access to runtime services (session/account/room etc.)."""

    @property
    @abstractmethod
    def commandsets(self) -> Sequence[Type[CommandSet]]:
        """Command sets exposed by this controller.

        Returns:
            A sequence of CommandSet types. Registries iterate these sets and register
            their `commands()` into the command catalog for this controller.

        Notes:
            Prefer returning *types* (not instances) for determinism and cheaper wiring.
        """
        raise NotImplementedError

    def connect_services(self, services: ServiceDirectory) -> None:
        """Inject the service directory.

        Args:
            services: The fully configured service directory provided by the platform.
        """
        self.services = services

    async def create_namespace(self, session: Session) -> Namespace:
        """Resolve the namespace for the given session.

        Args:
            session: Current runtime session.

        Returns:
            The resolved namespace for the session.
        """
        namespaces = self.services.get(NamespaceService)
        return await namespaces.from_session(session)

    async def on_before_resolve(self, session: Session) -> None:
        """Hook executed before command resolution.

        Intended use:
            - register dynamic commands for the current session
            - add context-sensitive aliases or shortcuts
            - adjust builtins for a specific program state

        This hook runs regardless of whether a valid command is found later.
        """

    async def on_before_run_command(self, session: Session, request: Request, command: Command) -> None:
        """Hook executed immediately before a command is run.

        Intended use:
            - enforce permissions
            - inject command context (batch id, controller id, tenant)
            - audit/tracing

        Args:
            session: Current runtime session.
            request: Parsed request that produced this command.
            command: The resolved command about to execute.
        """
        # default: no-op
        return None

    async def on_after_run_command(self, session: Session, request: Request, command: Command) -> None:
        """Hook executed immediately after a command finished.

        Intended use:
            - cleanup after a command
            - logging/audit
            - update controller-local state

        Args:
            session: Current runtime session.
            request: Parsed request that produced this command.
            command: The command that just executed.
        """
        # default: no-op
        return None

    async def on_cleanup(self, session: Session) -> None:
        """Hook executed after a command cycle, even if exceptions occurred.

        Intended use:
            - remove dynamic command groups
            - reset temporary state
            - undo session tweaks

        Args:
            session: Current runtime session.
        """
