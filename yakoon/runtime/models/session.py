from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Type
from uuid import uuid4

from yakoon.engine.io.output import Output
from yakoon.runtime.models.data import RuntimeSessionData, StorageSessionData


@dataclass
class BaseSession:
    """
    Represents a generic platform session.
    Handles persistent key-value data and domain-specific runtime context.
    """

    # ───── persistent fields (stored in DB/json) ─────

    id: str = field(default_factory=lambda: str(uuid4()))
    domain_id: str = ""
    lang: str = "de"

    # Persistent session state (e.g., account_id, domain flags)
    #: Session-wide persistent data storage (domain-aware dictionary).
    #: This is always reset before each command send to avoid runtime state leaks
    #: when using stateless memory-based sessions (e.g., for testing or batch processing).
    data_storage: StorageSessionData = field(default_factory=lambda: StorageSessionData()) #, repr=False, compare=False)

    # ───── transient runtime-only attributes ─────
    _cmd_groups: list[str] = field(default_factory=list, init=False, repr=False)
    _cmd_groups_dynamic: list[str] = field(default_factory=list, init=False, repr=False)
    _io: Output = field(default=None, init=False, repr=False)
    _data_runtime: Optional[RuntimeSessionData] = field(default=None, init=False, repr=False)

    def validate(self):
        if not self.id:
            raise ValueError("Id cannot be None or empty")

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

    @property
    def data_runtime(self) -> RuntimeSessionData:
        return self._data_runtime
    @data_runtime.setter
    def data_runtime(self, value):
        self._data_runtime = value

    def bind_io(self, io: Output):
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