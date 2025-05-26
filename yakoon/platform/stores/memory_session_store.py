from typing import Optional
from yakoon.engine.system.data import RuntimeSessionData
from yakoon.platform.runtime.session import PlatformSession
from yakoon.platform.stores.session_store import SessionStore


class InMemorySessionStore(SessionStore):

    def __init__(self, session_cls):
        self._sessions: dict[str, PlatformSession] = {}
        self._session_cls = session_cls

    async def get_by_id(self, session_id: str) -> Optional[PlatformSession]:
        if session_id in self._sessions:
            return self._sessions[session_id]

    async def get_or_create(self, session_id: str, **kwargs) -> tuple[PlatformSession, bool]:
        if session_id not in self._sessions:
            session: PlatformSession = self._session_cls(session_id)
            session.account_id = kwargs.get("account_id")
            self._sessions[session.id] = session
            return self._sessions[session.id], True
        session = self._sessions[session_id]
        session.data_runtime = RuntimeSessionData() # to avoid runtime state leaks
        return session, False

    async def delete(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)

    async def persist(self, session: PlatformSession) -> None:
        pass