from yakoon.base.runtime.session import Session, SessionState
from yakoon.base.models.key import Key
from yakoon.base.stores.base.base_store import BaseStore


class SessionService:
    
    def __init__(self, store: BaseStore):
        self._store = store
        self._services = None

    def set_services(self, services):
        self._services = services

    async def get(self, key: Key) -> Session | None:
        row = await self._store.get_by_key(key)
        if not row:
            return None

        state = SessionState.from_dict(row)
        return Session.from_state(state)

    async def save(self, session: Session) -> None:
        state = session.state
        row = state.to_dict()
        await self._store.save(row)

    async def get_or_create(self, key: Key, **kwargs) -> tuple[Session, bool]:
        """
        Returns an existing session if found, otherwise returns a new (unsaved) session.
        Does not persist the session automatically.
        """
        session = await self.get(key)
        if session:
            return session, False
        
        state = SessionState(key, **kwargs)
        session = Session.from_state(state)
        session.touch()
        await self.save(session)
 
        return session, True
 
    async def delete_by_key(self, key: Key):
        await self._store.delete_by_key(key)
 