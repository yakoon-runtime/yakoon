from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Sequence, Type

from yakoon.engine.core.commandset import CommandSet
from yakoon.engine.core.parser import Request
from yakoon.engine.core.router import CommandRouter

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yakoon.engine.system.session import BaseSession
    from yakoon.engine.core.command import Command


class BaseController(ABC):
    """
    Abstract base for all domain/platform definitions.
    Provides router and default session/command group config.
    """

    name: str = "unnamed"
    """Unique identifier used for command prefix resolution (e.g. mud:look, system:help)."""

    default_command_groups = []     

    def __init__(self):
        self.router = CommandRouter()
        self._register_all_commands()

    def _register_all_commands(self):
        for commands_set in self.commandsets:
            category = getattr(commands_set, "category", "system")
            self.router.register(self._get_value_with_prefix(category), commands_set)

    def _get_value_with_prefix(self, value: str) -> str:
        return f"{self.name}:{value}"
    
    def get_default_command_groups_with_prefix(self) -> list[str]:
        return [self._get_value_with_prefix(group) for group in self.default_command_groups]

    @property
    @abstractmethod
    def commandsets(self) -> Sequence[Type[CommandSet]]: ...

    async def on_before_send(self, session: BaseSession):
        """
        Hook called before any input is processed by the engine.
        Useful for logging, session validation, or input preprocessing.
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

    async def on_account_logout(self, session: BaseSession, account: Any):
        """
        Hook called before a user is logged out.
        Allows the domain to persist state, release resources, or perform cleanup.
        """
        pass

    async def on_after_send(self, session: BaseSession):
        """
        Hook called after input has been processed and all commands executed.
        Can be used for cleanup, analytics, or session state updates.
        """
