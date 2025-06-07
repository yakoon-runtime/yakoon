from yakoon.runtime.models.session import BaseSession
from yakoon.models.key import Key


class SessionService:
    
    def __init__(self, store):
        self._store = store
        self._services = None

    def set_services(self, services):
        self._services = services

    async def get_by_key(self, key: Key) -> BaseSession:
        row = await self._store.get_by_key(key)
        return BaseSession.from_row(row) if row else None

    async def get_or_new(self, key: Key, **kwargs) -> tuple[BaseSession, bool]:
        """
        Returns an existing session if found, otherwise returns a new (unsaved) session.
        Does not persist the session automatically.
        """
        session = await self.get_by_key(key)
        if session:
            return session
        return BaseSession(key=key, **kwargs)

    async def save(self, session: BaseSession):
        if not session.key.is_valid():
            prefix = session.key.get_prefix()             
            next_id = await self._services.counters.next(prefix)
            session.key = session.key.with_id(str(next_id))
        if not session.last_active:
            session.touch()
        await self._store.save(session.to_row())

    async def delete_by_key(self, key: Key):
        await self._store.delete_by_key(key)
 