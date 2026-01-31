from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional, Type
from datetime import datetime

from yakoon.base.models.entity import Entity
from yakoon.base.runtime.session.data import SessionData
from yakoon.base.runtime.session.output import Output


@dataclass
class Session(Entity):
    """
    Represents a generic session.
    Handles persistent key-value data and domain-specific runtime context.
    """

    lang: str = "de"
    last_active: str = None  # ISO-String (z. B. bei to_row()/from_row)
    
    tenant = "acme" #TODO: Only for now. later we have to move to sessiondata.

    _io: Output = field(default=None, init=False, repr=False)
    _cmd_groups: list[str] = field(default_factory=list, init=False, repr=False)
    _cmd_groups_dynamic: list[str] = field(default_factory=list, init=False, repr=False)

    _data_storage: SessionData = field(default_factory=lambda: SessionData()) #, repr=False, compare=False)
    _data_runtime: Optional[SessionData] = field(default_factory=lambda: SessionData(), init=False, repr=False)

    def validate(self):
        if not self.key:
            raise ValueError("Key cannot be None or empty")

    def touch(self):
        """Updates the timestamp of the last activity."""
        self.last_active = str(datetime.utcnow().isoformat())
   
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

    def ctx(self, group: str, key: str, default=None, *, persist: bool = False):
        """
        Unified context accessor.
        If runtime=True (default), uses volatile context.
        Otherwise uses persistent session data.
        """
        source = self._data_storage if persist else self._data_runtime
        return source.get(group, key, default)

    def set_ctx(self, group:str, key: str, value: Any, *, persist: bool = False):
        source = self._data_storage if persist else self._data_runtime
        source.set(group, key, value)

    def rem_ctx(self, group:str, key: str, *, persist: bool = False):
        source = self._data_storage if persist else self._data_runtime
        source.rem(group, key)

    def to_row(self) -> dict:
        row = super().to_row()
        row["data"] = self._data_storage.to_row()
        return row
    
    def set_active_controller(self, controller_id:str):
        self.set_ctx("state", "active_controller_id", controller_id, persist=True)
    def get_active_controller(self, default=None):
        return self.ctx("state", "active_controller_id", default, persist=True)

    @classmethod
    def from_row(cls, row: dict):
        data_raw = row.pop("data", {})
        obj = super().from_row(row)
        obj._data_storage = SessionData.from_row(data_raw)
        return obj

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