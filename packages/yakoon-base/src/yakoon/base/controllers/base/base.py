from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Sequence, Type
from typing import TYPE_CHECKING

from yakoon.base.commands.commandset import CommandSet
from yakoon.base.commands.parser import Request
from yakoon.base.runtime.system.registry import ServiceRegistry
from yakoon.base.runtime.system.router import ServiceRouter
from yakoon.base.runtime.views.template import TemplateSource

if TYPE_CHECKING:
    from yakoon.base.commands.command import MeshCommand
    from yakoon.base.models.namespace import Namespace
    from yakoon.base.runtime.session import BaseSession
    
class BaseController(ABC):
    """
    Abstract base for all domain/platform definitions.
    Provides router and default session/command group config.
    """

    id: str = "unnamed"
    """Unique identifier used for command prefix resolution (e.g. realm:look, system:help)."""

    default_command_groups = []    
    """Names of command groups that are automatically active for every session, 
    without requiring explicit permissions."""
 
    service_router: ServiceRouter = None
    """Provides bucket-based access to domain services (e.g. room, account, session). 
    Injected at runtime by the platform."""

    gateway: BaseController | None = None

    template_source: set[TemplateSource] = None

    @property
    @abstractmethod
    def commandsets(self) -> Sequence[Type[CommandSet]]: ...

    def __init__(self):
        self.service_router = ServiceRouter()

    def _get_value_with_prefix(self, value: str) -> str:
        return f"{self.id}:{value}"
    
    def get_default_command_groups_with_prefix(self) -> list[str]:
        return [self._get_value_with_prefix(group) for group in self.default_command_groups]

    async def get_namespace(self, session: BaseSession) -> Namespace:
        services = await self.get_system_services()
        return await services.namespaces.from_session(session)

    async def get_services(self) -> ServiceRegistry:
        return await self.service_router.get_registry(self.id)

    async def get_system_services(self) -> ServiceRegistry:
        if self.gateway is None or self.gateway.id == self.id:
            return await self.service_router.get_registry("system")
        return await self.gateway.service_router.get_registry("system")

    async def on_initialize(self, session: BaseSession):
        """
        Called after the controller has been fully constructed but before any commands are processed.

        Use this hook to perform asynchronous setup tasks such as loading data, initializing services,
        or validating infrastructure state (e.g., ensuring the admin account exists).

        This method is guaranteed to run once before the first engine tick or command dispatch.
        """
        pass

    async def on_before_resolve(self, session: BaseSession):
        """
        Hook called before command resolution.

        Use this to register dynamic commands for the current session,
        e.g. exits, room-specific actions or context-sensitive shortcuts.
        Executed regardless of whether a valid command is found.
        """

    async def on_before_run_command(self, session: BaseSession, request: Request, command: MeshCommand):
        """
        Hook called immediately before a single command is executed.
        Can be used to enforce permissions, inject context, or audit.
        """
        pass

    async def on_after_run_command(self, session: BaseSession, request: Request, command: MeshCommand):
        """
        Hook called immediately after a single command has been executed.
        Can be used for cleanup, logging, or updating domain state.
        """
        pass

    async def on_enter(self, session: BaseSession):
        """
        Called after a user switches into this domain (e.g. via @switch).
        Used to show welcome messages, check account requirements, or guide login flow.
        Override this in each domain to define entry behavior.
        """

    async def on_cleanup(self, session: BaseSession):
        """
        Always called after a command cycle, even if exceptions occurred.

        Use this to remove dynamic command groups, reset state,
        or undo temporary session changes.
        """


