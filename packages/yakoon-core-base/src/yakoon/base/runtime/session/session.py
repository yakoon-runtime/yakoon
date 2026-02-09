from __future__ import annotations

from datetime import datetime, timezone
from dataclasses import dataclass, asdict, field
from typing import Mapping, Optional, Any

from yakoon.base.models.key import Key
from yakoon.base.models.mode import InteractionMode
from yakoon.base.models.perm import PermissionSet
from yakoon.base.runtime.output.event import OutputEvent
from yakoon.base.models.format import OutputFormat


@dataclass
class SessionState:
    """
    Persistable session state.

    Contains only serializable data.
    The session key is part of the state and is immutable for the lifetime
    of the session.
    """
    key: Key

    active_controller_id: str | None = None
    account_key: str | None = None
    username: str | None = None
    last_active: datetime | None = None
    lang: Optional[str] = "de"

    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        if self.last_active:
            d["last_active"] = self.last_active.astimezone(timezone.utc).isoformat()
        else:
            d["last_active"] = None
        if self.key:
            d["key"] = str(self.key)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "SessionState":
        if not d or "key" not in d:
            raise ValueError("SessionState requires a 'key'")

        d = dict(d)
        raw_key = d.pop("key")
        raw_last_active = d.pop("last_active", None)
        state = cls(key=Key.from_str(raw_key),**d)
        if raw_last_active:
            state.last_active = datetime.fromisoformat(raw_last_active)

        return state


@dataclass
class SessionRuntime:
    permissions: PermissionSet = field(default_factory=PermissionSet)
    data: dict[str, Any] = field(default_factory=dict)
    interaction_mode: InteractionMode = InteractionMode(InteractionMode.WIZARD)
    output_format: OutputFormat = OutputFormat(OutputFormat.PLAIN)
    signals: set[str] = field(default_factory=set)
    io: object | None = None


class Session:
    """
    Represents a single interactive session.

    A Session is a runtime façade that combines:
    - a persistent SessionState (identity, controller, timestamps)
    - a volatile SessionRuntime (IO bindings, signals, host-specific state)

    The session itself is not persisted directly.
    Only its state is serializable and stored by the SessionService.
    """

    def __init__(self, state: SessionState):
        """
        Creates a new session with an empty state and fresh runtime context.

        Args:
            key (Key): Unique identifier of the session.
        """
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

    # ---- interaction_mode ----

    @property
    def interaction_mode(self) -> InteractionMode:
        return self._runtime.interaction_mode

    @interaction_mode.setter
    def interaction_mode(self, value: InteractionMode) -> None:
        if value.value not in InteractionMode.values():
            raise ValueError(f"Invalid interaction_mode: {value.value}")
        self._runtime.interaction_mode = value

    # ---- output_format ----

    @property
    def output_format(self) -> OutputFormat:
        return self._runtime.output_format

    @output_format.setter
    def output_format(self, value: OutputFormat) -> None:
        if value.value not in OutputFormat.values():
            raise ValueError(f"Invalid output_format: {value.value}")
        self._runtime.output_format = value

    def set_permissions(self, permset: PermissionSet) -> None:
        self._runtime.permissions = permset

    @classmethod
    def from_state(cls, state: SessionState) -> "Session":
        """
        Reconstructs a session from a previously persisted SessionState.

        A new runtime context is created automatically.
        This method is typically used by SessionService when loading sessions
        from storage.

        Args:
            state (SessionState): The persisted session state.

        Returns:
            Session: A fully initialized session with fresh runtime data.
        """
        return cls(state)

    def touch(self) -> None:
        """
        Marks the session as recently active.

        Updates the last_active timestamp in the persistent session state.
        This should be called on user interaction (e.g. dispatch, prompt input),
        not on every internal execution step.
        """
        self._state.last_active = datetime.now(timezone.utc)

    def bind_io(self, io):
        """
        Binds an output channel to the session runtime.

        This is a runtime-only operation and is not persisted.
        Different hosts (console, WebSocket, telnet) may bind different IO adapters.

        Args:
            io: Output adapter providing out() and err() coroutines.
        """
        self._runtime.io = io

    def set_username(self, username: str | None):
        """
        Sets or clears the username associated with this session.

        Args:
            username (str | None): The username to set, or None to clear it.
        """
        self._state.username = username

    def get_username(self) -> str | None:
        """
        Returns the current username associated with the session.

        Returns:
            str | None: The username, or None if no identity is set.
        """
        return self._state.username

    def set_active_controller(self, controller_id: str | None) -> None:
        """
        Sets the active controller for the session.

        The active controller determines which command set is currently in scope
        (e.g. shell, auth, domain-specific controllers).

        Args:
            controller_id (str | None): Controller identifier or None.
        """
        self._state.active_controller_id = controller_id

    def get_active_controller(self, default=None):
        """
        Returns the currently active controller.

        Args:
            default: Value to return if no controller is active.

        Returns:
            The active controller ID or the provided default.
        """
        return self._state.active_controller_id or default

    def set_identity(self, account_key, username: str) -> None:
        """
        Assigns an authenticated identity to the session.

        This method sets both the account key and username in the persistent
        session state.

        Args:
            account_key: Unique identifier of the account.
            username (str): Human-readable username.
        """
        self._state.account_key = str(account_key)
        self._state.username = username

    def clear_identity(self) -> None:
        """
        Removes any authenticated identity from the session.

        This effectively logs the user out while keeping the session alive.
        """
        self._state.account_key = None
        self._state.username = None

    def has_identity(self) -> bool:
        """
        Checks whether the session currently has an authenticated identity.

        Returns:
            bool: True if an account is associated with the session.
        """
        return self._state.account_key is not None

    def signal(self, name: str) -> None:
        """
        Emits a runtime-only signal for the session.

        Signals are used to communicate intentions to the host
        (e.g. quit application, logout, reload shell).
        They are not persisted.

        Args:
            name (str): Signal identifier.
        """
        self._runtime.signals.add(name)

    def has_signal(self, name: str) -> bool:
        """
        Checks whether a given signal is currently set.

        Args:
            name (str): Signal identifier.

        Returns:
            bool: True if the signal is present.
        """
        return name in self._runtime.signals

    def clear_signals(self) -> None:
        """
        Clears all runtime signals associated with the session.
        """
        self._runtime.signals.clear()

    async def emit(self, text: str, *,
                   mime: str = "text/plain", channel: str = "main",
                   op: str = "append", region: str = "output", 
                   meta: Optional[Mapping[str, Any]] = None,    ) -> None:
        """
        Emits a plain output message via the session's output channel.

        This is typically used for normal command output.

        Args:
            text (str): The message to emit.
        """
        evt = OutputEvent(text=text, mime=mime, 
                          channel=channel, op=op, region=region, 
                          meta=dict(meta or {}),)
        await self._runtime.io.out(evt)


    async def notify(self, text: str, *,
                   mime: str = "text/plain", channel: str = "main",
                   op: str = "append", region: str = "information", 
                   meta: Optional[Mapping[str, Any]] = None,    ) -> None:
        """
        Emits a non-error informational status message.

        This is commonly used for confirmations or system notifications.

        Args:
            text (str): The status message to display.
        """
        evt = OutputEvent(text=text, mime=mime, 
                          channel=channel, op=op, region=region, 
                          meta=dict(meta or {}),)
        await self._runtime.io.out(evt)

    async def fail(self, text: str, *,
                   mime: str = "text/plain", channel: str = "main",
                   op: str = "append", region: str = "status", 
                   meta: Optional[Mapping[str, Any]] = None,    ) -> None:
        """
        Emits an error or failure message.

        Args:
            text (str): The error message to display.
        """
        evt = OutputEvent(text=text, mime=mime, 
                          channel=channel, op=op, region=region, 
                          meta=dict(meta or {}),)
        await self._runtime.io.err(evt)
