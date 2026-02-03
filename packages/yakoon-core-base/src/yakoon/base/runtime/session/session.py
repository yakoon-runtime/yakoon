from __future__ import annotations

from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

from yakoon.base.models.key import Key


@dataclass
class SessionState:

    key: Key | None = None
    last_active: datetime | None = None
    active_controller_id: Optional[str] = None
    account_key: Optional[str] = None
    username: Optional[str] = None
    lang: Optional[str] = "de"
    data: Dict[str, Any] = None 
    
    def to_dict(self) -> dict:
        d = asdict(self)
        if d["data"] is None:
            d["data"] = {}
        if self.last_active:
            d["last_active"] = self.last_active.astimezone(timezone.utc).isoformat()
        else:
            d["last_active"] = None
        if self.key:
            d["key"] = str(self.key)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "SessionState":
       d = dict(d or {})
       d.setdefault("data", {})
       raw_key = d.pop("key", None)
       raw_last_active = d.pop("last_active", None)
       obj = cls(**d)
       if raw_key:
           obj.key = Key.from_str(raw_key)
       if raw_last_active:
           obj.last_active = datetime.fromisoformat(raw_last_active)

       return obj


class SessionRuntime:
    
    def __init__(self):
        self.data: dict[str, object] = {}
        self.signals: set[str] = set()
        self.io = None   


class Session:
    """
    Represents a single interactive session.

    A Session is a runtime façade that combines:
    - a persistent SessionState (identity, controller, timestamps)
    - a volatile SessionRuntime (IO bindings, signals, host-specific state)

    The session itself is not persisted directly.
    Only its state is serializable and stored by the SessionService.
    """

    def __init__(self, key: Key):
        """
        Creates a new session with an empty state and fresh runtime context.

        Args:
            key (Key): Unique identifier of the session.
        """
        self._state = SessionState(key=key, data={})
        self._runtime = SessionRuntime()

    @property
    def lang(self) -> str:
        return self._state.lang        

    @property
    def key(self) -> Key:
        return self._state.key        

    @classmethod
    def from_state(cls, key: Key, state: SessionState) -> "Session":
        """
        Reconstructs a session from a previously persisted SessionState.

        A new runtime context is created automatically.
        This method is typically used by SessionService when loading sessions
        from storage.

        Args:
            key (Key): The session identifier.
            state (SessionState): The persisted session state.

        Returns:
            Session: A fully initialized session with fresh runtime data.
        """
        s = cls(None)
        s._state = state
        s._state.key = key
        return s

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

    def get_username(self, default: str = "") -> str:
        """
        Returns the current username or a default value.

        Args:
            default (str): Value returned if no username is set.

        Returns:
            str: The username or the default value.
        """
        return self._state.username or default

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

    def clear_signal(self, name: str) -> None:
        """
        Removes a specific runtime signal from the session.

        Args:
            name (str): Signal identifier.
        """
        self._runtime.signals.discard(name)

    def clear_signals(self) -> None:
        """
        Clears all runtime signals associated with the session.
        """
        self._runtime.signals.clear()

    async def emit(self, text: str):
        """
        Emits a plain output message via the session's output channel.

        This is typically used for normal command output.

        Args:
            text (str): The message to emit.
        """
        await self._runtime.io.out(text)

    async def notify(self, text: str):
        """
        Emits a non-error informational status message.

        This is commonly used for confirmations or system notifications.

        Args:
            text (str): The status message to display.
        """
        await self._runtime.io.out(f"> i: {text}")

    async def fail(self, text: str):
        """
        Emits an error or failure message.

        Args:
            text (str): The error message to display.
        """
        await self._runtime.io.err(f"> e: {text}")
