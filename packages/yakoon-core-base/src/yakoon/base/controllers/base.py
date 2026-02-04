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
    from yakoon.base.models.ns import Namespace
    from yakoon.base.runtime.session import Session
    
    
class BaseController(ABC):
    """
    Abstract base for all controllers.
    """
    
    id: str = "unnamed"
    """Unique identifier used for command prefix resolution (e.g. realm:look, system:help)."""

    is_shell: bool = False
    is_listed: bool = True
    is_activatable: bool = True

    shell_builtins = {}
    """Shell builtin commands are always available and independent 
    of the active program context."""

    default_command_groups = []    
    """Names of command groups that are automatically active for every session, 
    without requiring explicit permissions."""
 
    services: ServiceDirectory = None
    """Provides bucket-based access to services (e.g. room, account, session). 
    Injected at runtime by the platform."""

    template_source: TemplateSource = None
    """TemplateSource for all views of this controller (command output and man pages).
    View selection is done by template key conventions (cmd_*, man_*)."""

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

    async def on_cleanup(self, session: Session):
        """
        Always called after a command cycle, even if exceptions occurred.

        Use this to remove dynamic command groups, reset state,
        or undo temporary session changes.
        """


