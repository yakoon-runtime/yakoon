from yakoon.base.runtime.session import Session
from yakoon.base.models.key import Key
from yakoon.base.runtime.session.state import SessionState
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

        # strip store meta
        data = {k: v for k, v in row.items() if not k.startswith("__")}
        state = SessionState.from_dict(data)

        # build a runtime session (fresh runtime)
        return Session.from_state(key=key, state=state)

    async def save(self, session: Session) -> None:
        state = session.state
        row = state.to_dict()
        row["__key__"] = str(session.key)
        row["__scope__"] = session.key.namespace.to_str()
        await self._store.save(row)

    async def get_or_create(self, key: Key, **kwargs) -> tuple[Session, bool]:
        """
        Returns an existing session if found, otherwise returns a new (unsaved) session.
        Does not persist the session automatically.
        """
        session = await self.get(key)
        if session:
            return session, False
        
        state = SessionState.from_dict(kwargs)
        session = Session.from_state(key, state)
        session.touch()
        await self.save(session)
 
        return session, True
 
    async def delete_by_key(self, key: Key):
        await self._store.delete_by_key(key)
 