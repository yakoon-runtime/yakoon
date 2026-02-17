# yakoon/base/runtime/session/session.py
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any

from yakoon.base.models.key import Key
from yakoon.base.models.perm import PermissionSet
from yakoon.base.runtime.output.event import OutputEvent


@dataclass
class SessionState:
    key: Key
    active_controller_id: str | None = None
    account_key: str | None = None
    username: str | None = None
    last_active: datetime | None = None
    lang: str | None = "de"
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        if self.last_active:
            d["last_active"] = self.last_active.astimezone(UTC).isoformat()
        else:
            d["last_active"] = None
        if self.key:
            d["key"] = str(self.key)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> SessionState:
        if not d or "key" not in d:
            raise ValueError("SessionState requires a 'key'")

        d = dict(d)
        raw_key = d.pop("key")
        raw_last_active = d.pop("last_active", None)
        state = cls(key=Key.from_str(raw_key), **d)
        if raw_last_active:
            state.last_active = datetime.fromisoformat(raw_last_active)
        return state


@dataclass
class SessionRuntime:
    permissions: PermissionSet = field(default_factory=PermissionSet)
    signals: set[str] = field(default_factory=set)
    io: object | None = None
    meta: dict[str, Any] = field(default_factory=dict)


class Session:
    """
    Session output contract is strict:
      - emit/notify/fail accept ONLY ViewSpec mappings (kind='view')
      - mime is always application/yakoon.view+json
    """

    VIEW_MIME = "application/yakoon.view+json"

    def __init__(self, state: SessionState):
        self._state = state
        self._runtime = SessionRuntime()

    @property
    def lang(self) -> str:
        return self._state.lang

    @property
    def key(self) -> Key:
        return self._state.key

    @property
    def state(self) -> SessionState:
        return self._state

    @property
    def permissions(self) -> PermissionSet:
        return self._runtime.permissions

    def set_permissions(self, permset: PermissionSet) -> None:
        self._runtime.permissions = permset

    @classmethod
    def from_state(cls, state: SessionState) -> Session:
        return cls(state)

    def touch(self) -> None:
        self._state.last_active = datetime.now(UTC)

    def bind_io(self, io):
        self._runtime.io = io

    def set_username(self, username: str | None):
        self._state.username = username

    def get_username(self) -> str | None:
        return self._state.username

    def set_active_controller(self, controller_id: str | None) -> None:
        self._state.active_controller_id = controller_id

    def get_active_controller(self, default=None):
        return self._state.active_controller_id or default

    def set_identity(self, account_key, username: str) -> None:
        self._state.account_key = str(account_key)
        self._state.username = username

    def clear_identity(self) -> None:
        self._state.account_key = None
        self._state.username = None

    def has_identity(self) -> bool:
        return self._state.account_key is not None

    def signal(self, name: str) -> None:
        self._runtime.signals.add(name)

    def has_signal(self, name: str) -> bool:
        return name in self._runtime.signals

    def clear_signals(self) -> None:
        self._runtime.signals.clear()

    # ----------------------------
    # Strict View output
    # ----------------------------

    def _ensure_view(self, payload: Any) -> dict[str, Any]:
        if not isinstance(payload, Mapping):
            raise TypeError("Session output must be a ViewSpec mapping (kind='view').")
        view = dict(payload)
        if view.get("kind") != "view":
            raise TypeError("Session output must be a ViewSpec with kind='view'.")
        return view

    async def emit(
        self,
        payload: Any,
        *,
        channel: str = "main",
        op: str = "append",
        region: str = "output",
        meta: Mapping[str, Any] | None = None,
    ) -> None:
        view = self._ensure_view(payload)
        evt = OutputEvent(
            payload=view,
            mime=self.VIEW_MIME,
            channel=channel,
            op=op,
            region=region,
            meta=dict(meta or {}),
        )
        await self._runtime.io.out(evt)

    async def notify(
        self,
        payload: Any,
        *,
        channel: str = "main",
        op: str = "append",
        region: str = "information",
        meta: Mapping[str, Any] | None = None,
    ) -> None:
        view = self._ensure_view(payload)
        evt = OutputEvent(
            payload=view,
            mime=self.VIEW_MIME,
            channel=channel,
            op=op,
            region=region,
            meta=dict(meta or {}),
        )
        await self._runtime.io.out(evt)

    async def fail(
        self,
        payload: Any,
        *,
        channel: str = "main",
        op: str = "append",
        region: str = "status",
        meta: Mapping[str, Any] | None = None,
    ) -> None:
        view = self._ensure_view(payload)
        evt = OutputEvent(
            payload=view,
            mime=self.VIEW_MIME,
            channel=channel,
            op=op,
            region=region,
            meta=dict(meta or {}),
        )
        await self._runtime.io.err(evt)
