from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Sequence, Type
from typing import TYPE_CHECKING

from yakoon.core.commandset import CommandSet
from yakoon.core.parser import Request
from yakoon.engine.router import CommandRouter
from yakoon.services.registry import ServiceRegistry
from yakoon.services.router import ServiceRouter

if TYPE_CHECKING:
    from yakoon.runtime.models.session import BaseSession
    from yakoon.core.domain.registry import BaseDomainRegistry
    from yakoon.core.command import Command


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
 
    service_router: ServiceRouter | None = None
    """Provides bucket-based access to domain services (e.g. room, account, session). 
    Injected at runtime by the platform."""

    gateway: BaseController | None = None

    def __init__(self):
        self.router = CommandRouter()
        self._register_all_commands()

    def _register_all_commands(self):
        for commands_set in self.commandsets:
            category = getattr(commands_set, "category", "system")
            self.router.register(self._get_value_with_prefix(category), commands_set)

    def _get_value_with_prefix(self, value: str) -> str:
        return f"{self.id}:{value}"
    
    def get_default_command_groups_with_prefix(self) -> list[str]:
        return [self._get_value_with_prefix(group) for group in self.default_command_groups]

    def bind_service_router(self, router: ServiceRouter):
        self.router = router

    @property
    @abstractmethod
    def commandsets(self) -> Sequence[Type[CommandSet]]: ...

    async def get_domain_services(self) -> ServiceRegistry:
        return await self.service_router.get_registry(self.id)

    async def get_gateway_services(self) -> ServiceRegistry:
        if self.gateway is None or self.gateway.id == self.id:
            return await self.service_router.get_registry(self.id)
        return await self.gateway.service_router.get_registry(self.gateway.id)

    async def get_controller_registry(self) -> BaseDomainRegistry:
        gateway = self.gateway if self.gateway else self 
        if hasattr(gateway, "controller_registry"):
            return gateway.controller_registry
        return None

    async def on_initialize(self, session: BaseSession):
        """
        Called after the controller has been fully constructed but before any commands are processed.

        Use this hook to perform asynchronous setup tasks such as loading data, initializing services,
        or validating infrastructure state (e.g., ensuring the admin account exists).

        This method is guaranteed to run once before the first engine tick or command dispatch.
        """
        pass

    async def on_gateway_validate(self, session: BaseSession):
        """
        Platform-level pre-send hook, called before request parsing.

        Used to prepare session context (e.g., account, locale, dynamic commands).
        Only invoked if this controller is the registered `system` controller.
        """
        pass

    async def on_before_resolve(self, session: BaseSession):
        """
        Hook called before command resolution.

        Use this to register dynamic commands for the current session,
        e.g. exits, room-specific actions or context-sensitive shortcuts.
        Executed regardless of whether a valid command is found.
        """

    async def on_before_run_command(self, session: BaseSession, request: Request, command: Command):
        """
        Hook called immediately before a single command is executed.
        Can be used to enforce permissions, inject context, or audit.
        """
        pass

    async def on_after_run_command(self, session: BaseSession, request: Request, command: Command):
        """
        Hook called immediately after a single command has been executed.
        Can be used for cleanup, logging, or updating domain state.
        """
        pass

    async def on_account_login(self, session: BaseSession, account: Any):
        """
        Hook called after a user successfully logs in.
        Allows the domain to perform setup such as loading player state or emitting welcome messages.
        """
        pass

    async def on_enter(self, session: BaseSession):
        """
        Called after a user switches into this domain (e.g. via @switch).
        Used to show welcome messages, check account requirements, or guide login flow.
        Override this in each domain to define entry behavior.
        """

    async def on_account_logout(self, session: BaseSession, account: Any):
        """
        Hook called before a user is logged out.
        Allows the domain to persist state, release resources, or perform cleanup.
        """
        pass

    async def on_cleanup(self, session: BaseSession):
        """
        Always called after a command cycle, even if exceptions occurred.

        Use this to remove dynamic command groups, reset state,
        or undo temporary session changes.
        """

    async def on_gateway_finalize(self, session: BaseSession):
        """
        Platform-level post-send hook, called after command runing.

        Used to cleanup session context (e.g., account, locale, dynamic commands).
        Only invoked if this controller is the registered `system` controller.
        """
        pass


