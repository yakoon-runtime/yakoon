from typing import Optional
from yakoon.domains.platform.runtime.session import PlatformSession
from yakoon.domains.platform.stores.base.session import BaseSessionStore


class InMemorySessionStore(BaseSessionStore):

    def __init__(self):
        self._sessions: dict[str, PlatformSession] = {}

    async def get_by_id(self, session_id: str) -> Optional[PlatformSession]:
        if session_id in self._sessions:
            return self._sessions[session_id]

    async def get_or_create(self, session_id: str, **kwargs) -> tuple[PlatformSession, bool]:
        if session_id not in self._sessions:
            session = PlatformSession(session_id)
            self._sessions[session.id] = session
            return self._sessions[session.id], True
        session = self._sessions[session_id]
        return session, False

    async def delete_by_id(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)

    async def save(self, session: PlatformSession) -> None:
        pass