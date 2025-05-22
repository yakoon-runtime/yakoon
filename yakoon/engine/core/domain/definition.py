from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Sequence, Type

from yakoon.engine.core.commandset import CommandSet
from yakoon.engine.core.parser import Request
from yakoon.engine.services.session_service import BaseSessionService

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yakoon.engine.system.session import BaseSession
    from yakoon.engine.core.command import Command


class DomainDefinition(ABC):

    default_command_groups = []     
    sessions: BaseSessionService

    @property
    @abstractmethod
    def commandsets(self) -> Sequence[Type[CommandSet]]: ...

    async def on_before_send(self, session: BaseSession):
        """
        Hook that is called before any command(s) are processed.
        Can be used to prepare or validate the session state.
        This is triggered once per input string (before command batching).
        """
        pass

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

    async def on_after_send(self, session: BaseSession):
        """
        Hook called after all commands for a given input string have been processed.
        Useful for session cleanup or state finalization.
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
