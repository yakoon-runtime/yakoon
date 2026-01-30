from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Sequence, Type
from typing import TYPE_CHECKING

from yakoon.base.commands.commandset import CommandSet
from yakoon.base.commands.request import Request
from yakoon.base.ports import NamespaceService
from yakoon.base.directories.service import ServiceDirectory
from yakoon.base.descriptors.template import TemplateSource

if TYPE_CHECKING:
    from yakoon.base.commands.command import Command
    from yakoon.base.models.namespace import Namespace
    from yakoon.base.runtime.session import Session
    
class BaseController(ABC):
    """
    Abstract base for all controllers.
    Provides router and default session/command group config.
    """
    
    id: str = "unnamed"
    """Unique identifier used for command prefix resolution (e.g. realm:look, system:help)."""

    is_gateway = False

    default_command_groups = []    
    """Names of command groups that are automatically active for every session, 
    without requiring explicit permissions."""
 
    services: ServiceDirectory = None
    """Provides bucket-based access to services (e.g. room, account, session). 
    Injected at runtime by the platform."""

    template_source: set[TemplateSource] = None

    @property
    @abstractmethod
    def commandsets(self) -> Sequence[Type[CommandSet]]: ...

    def __init__(self):
        self.services = ServiceDirectory()

    def connect_services(self, services: ServiceDirectory):
        self.services = services
    
    async def create_namespace(self, session: Session) -> Namespace:
        namespaces = self.services.get(NamespaceService)
        
        return await namespaces.from_session(session)
    
    async def on_initialize(self, session: Session):
        """
        Called after the controller has been fully constructed but before any commands are processed.

        Use this hook to perform asynchronous setup tasks such as loading data, initializing services,
        or validating infrastructure state (e.g., ensuring the admin account exists).

        This method is guaranteed to run once before the first engine tick or command dispatch.
        """
        pass

    async def on_before_resolve(self, session: Session):
        """
        Hook called before command resolution.

        Use this to register dynamic commands for the current session,
        e.g. exits, room-specific actions or context-sensitive shortcuts.
        Executed regardless of whether a valid command is found.
        """

    async def on_before_run_command(self, session: Session, request: Request, command: Command):
        """
        Hook called immediately before a single command is executed.
        Can be used to enforce permissions, inject context, or audit.
        """
        pass

    async def on_after_run_command(self, session: Session, request: Request, command: Command):
        """
        Hook called immediately after a single command has been executed.
        Can be used for cleanup, logging, or updating domain state.
        """
        pass

    async def on_enter(self, session: Session):
        """
        Called after a user switches into this domain (e.g. via @switch).
        Used to show welcome messages, check account requirements, or guide login flow.
        Override this in each domain to define entry behavior.
        """

    async def on_cleanup(self, session: Session):
        """
        Always called after a command cycle, even if exceptions occurred.

        Use this to remove dynamic command groups, reset state,
        or undo temporary session changes.
        """


