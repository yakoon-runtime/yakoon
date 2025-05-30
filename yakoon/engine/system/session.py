from __future__ import annotations
from typing import Optional, Type
from uuid import uuid4

from typing import TYPE_CHECKING

from yakoon.engine.core.io.adapter import IOAdapter
from yakoon.engine.system.data import RuntimeSessionData, StorageSessionData

if TYPE_CHECKING:
    from yakoon.engine.core.domain.controller import BaseController
    from yakoon.engine.system.context import Context


class BaseSession(object):
    """
    Represents a generic platform session.
    Handles persistent key-value data and domain-specific runtime context.
    """

    def __init__(self, id: str):
        """
        Constructs a new session.
        """
        self.id = id or str(uuid4())
        self.lang: str = "de"

        self._cmd_groups = []
        self._cmd_groups_dynamic = []
        self._context:Context = None
        self._domain:BaseController = None
        self._io: IOAdapter = None

        # Persistent session state (e.g., account_id, domain flags)
        #: Session-wide persistent data storage (domain-aware dictionary).
        #: This is always reset before each command send to avoid runtime state leaks
        #: when using stateless memory-based sessions (e.g., for testing or batch processing).
        self.data_storage: StorageSessionData = StorageSessionData()
        # Domain-specific runtime data (e.g., Character, Document, etc.)
        self.data_runtime: Optional[RuntimeSessionData] = None

    @property
    def ctx(self) -> Context:
        return self._context

    @property
    def domain(self) -> BaseController:
        return self._domain
    @domain.setter
    def domain(self, value):
        self._domain = value

    @property
    def cmd_groups(self) -> list[Type[str]]:
        return self._cmd_groups
    @cmd_groups.setter
    def cmd_groups(self, value):
        self._cmd_groups = value

    @property
    def cmd_groups_dynamic(self) -> list[Type[str]]:
        return self._cmd_groups_dynamic
    @cmd_groups_dynamic.setter
    def cmd_groups_dynamic(self, value):
        self._cmd_groups_dynamic = value

    def bind_context(self, context: Context):
        self._context = context

    def bind_io(self, io: IOAdapter):
        self._io = io

    async def emit(self, text: str):
        """
        Outputs a plain text message via the session's output channel.

        Args:
            text (str): The message to emit.
        """
        await self._io.out(text)

    async def notify(self, text: str):
        """
        Emits a status message (e.g. success, ready) with a visual marker.

        Args:
            text (str): The status message to display.
        """
        await self._io.out(f"> i: {text}")

    async def fail(self, text: str):
        """
        Emits an error or failure message with an error marker.

        Args:
            text (str): The error message to display.
        """
        await self._io.err(f"> e: {text}")

    async def dispatch(self, input_str: str):
        """
        Sends a command for execution using the current session context.

        Args:
            input_str (str): The command string to dispatch.
        """
        await self.ctx.dispatch(self, input_str, self._io)
