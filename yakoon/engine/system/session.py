from __future__ import annotations
from typing import Any, Coroutine, Callable, Optional, Type, TypeVar
from uuid import uuid4

from typing import TYPE_CHECKING

from yakoon.engine.system.data import RuntimeSessionData, StorageSessionData

if TYPE_CHECKING:
    from yakoon.engine.core.domain.controller import BaseController
    from yakoon.engine.system.context import Context

Text = TypeVar('Text', str, bytes)
PrintMessage = Callable[[Text], Coroutine]
PrintError = Callable[[Exception], Coroutine]


class BaseSession(object):
    """
    Represents a generic platform session.
    Handles persistent key-value data and domain-specific runtime context.
    """

    #: Output callback function used for normal messages.
    #: Typically sends text to the user interface (e.g., console, webclient, telnet).
    out: PrintMessage

    #: Output callback function used for error messages.
    #: Used to signal problems, warnings, or command feedback.
    err: PrintError

    def __init__(self, id: str):
        """
        Constructs a new session.
        """
        self.id = id or str(uuid4())
        self._cmd_groups = []
        self._cmd_groups_dynamic = []
        self._context:Context = None
        self._domain:BaseController = None

        #: Output callback for normal messages (must be assigned before use)
        self.out: Optional[PrintMessage] = None

        #: Output callback for error messages (must be assigned before use)
        self.err: Optional[PrintError] = None

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

    async def send_msg(self, text: str):
        assert self.out is not None, "Output function not set"
        await self.out(text)

    async def send_status(self, text: str):
        assert self.out is not None, "Output function not set"
        await self.out(f"✅ {text}")

    async def send_error(self, text: str):
        assert self.out is not None, "Output function not set"
        await self.err(f"❌ {text}")

    async def send_cmd(self, input_str: str):
        await self.ctx.send_cmd(self, input_str, self.out, self.err)