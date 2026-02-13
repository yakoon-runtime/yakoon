from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from yakoon.base.models.command import CommandKind, CommandVisibility
from yakoon.base.ports import NamespaceService, Presenter, PresenterService

if TYPE_CHECKING:
    from typing import Any

    from yakoon.base.commands.request import Request
    from yakoon.base.controllers.base import BaseController
    from yakoon.base.directories.service import ServiceDirectory
    from yakoon.base.models.ns import Namespace
    from yakoon.base.runtime.session.session import Session


class CmdNotFound(LookupError):
    """Raised when a command cannot be resolved.

    This is intentionally a LookupError to align with Python's lookup semantics.
    Dispatchers typically map this to a user-facing "unknown command" message.
    """


class WorkflowContextRequired(RuntimeError):
    """Raised when a workflow-only command is invoked without a workflow batch."""


@dataclass(frozen=True, slots=True)
class CommandContext:
    """Runtime context for command execution.

    Attributes:
        controller: Active controller providing services and template configuration.
        batch_id: Workflow batch identifier, if the command is executed within a workflow.
    """

    controller: BaseController
    batch_id: str | None = None

    @property
    def is_batch(self) -> bool:
        """True if the command executes within a workflow batch."""
        return self.batch_id is not None


@dataclass(frozen=True, slots=True)
class CommandResult:
    """Structured result returned by `Command.run()`.

    Public frameworks live and die by stable contracts. A structured result makes it
    possible to evolve behavior without breaking callers.

    Attributes:
        message: Optional short human-readable message (for logs/UI).
        payload: Optional structured data (engine/UI decides how to display/use it).
        next_command: Optional command key to suggest/trigger next (useful in flows).
        meta: Optional metadata for tracing/debugging (should be JSON-serializable).
    """

    message: str | None = None
    payload: Any = None
    next_command: str | None = None
    meta: dict[str, Any] | None = None


class Command(ABC):
    """Base class for all executable commands.

    Subclasses define the command's identity via class attributes and implement `run()`.

    Public API contract:
        - Commands are cheap to instantiate and should remain stateless.
        - All dependencies are resolved via `context.controller.services`.
        - `run()` returns a `CommandResult` (never raw strings / ad-hoc dicts).

    Required class attributes:
        key: Unique command identifier (often namespaced).
    """

    # Public identity
    key: str
    aliases: tuple[str, ...] = ()

    # Execution metadata
    kind: CommandKind = CommandKind.USER
    visibility: CommandVisibility = CommandVisibility.NORMAL

    # If True, dispatcher or command must enforce workflow context.
    requires_workflow: bool = False

    # Runtime-provided
    context: CommandContext

    # Optional template prefix (controller-dependent)
    template_prefix: str = ""

    @property
    def services(self) -> ServiceDirectory:
        """Service directory exposed by the active controller."""
        return self.context.controller.services

    def ensure_workflow_context(self) -> str:
        """Return the workflow batch id or raise if missing.

        Returns:
            The workflow batch id.

        Raises:
            WorkflowContextRequired: If the command requires workflow context but none exists.
        """
        if not self.context.is_batch:
            raise WorkflowContextRequired(
                f"Command '{self.key}' requires a workflow batch context."
            )
        # mypy: batch_id is Optional[str], but context.is_batch guarantees it exists
        return self.context.batch_id  # type: ignore[return-value]

    def get_template_path(self) -> str:
        """Compute the template path for this command within the controller."""
        template_sub_path = self.context.controller.template_source.template_sub_path
        return str(Path(template_sub_path).joinpath(self.template_prefix, self.key))

    async def get_namespace(self, session: Session) -> Namespace:
        """Resolve the namespace for the current session."""
        namespaces = self.services.get(NamespaceService)
        return await namespaces.from_session(session)

    async def get_presenter(self, session: Session) -> Presenter:
        """Create a presenter bound to this command's template path and session."""
        presenter = self.services.get(PresenterService)
        return await presenter.create_presenter(
            self.context.controller.template_source.package,
            self.get_template_path(),
            session,
        )

    @abstractmethod
    async def run(self, session: Session, request: Request) -> CommandResult:
        """Execute the command and return a structured result.

        Notes:
            - Do not raise user-facing errors for normal control flow. Prefer encoding
              outcomes in CommandResult.
            - Reserve exceptions for programmer errors, missing context, or truly
              exceptional states.
        """
        raise NotImplementedError


class WfCommand(Command):
    """Base class for workflow-only (internal) commands."""

    kind = CommandKind.WORKFLOW
    visibility = CommandVisibility.DEVELOPER
    requires_workflow = True
