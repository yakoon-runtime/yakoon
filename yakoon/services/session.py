from yakoon.runtime.models.session import BaseSession
from yakoon.models.key import Key


class SessionService:
    
    def __init__(self, store):
        self.store = store

    async def get_by_key(self, key: Key) -> BaseSession:
        row = await self.store.get_by_key(key)
        return BaseSession.from_row(row) if row else None

    async def get_or_create(self, key: Key, **kwargs) -> tuple[BaseSession, bool]:
        session = await self.get_by_key(key)
        if session:
            created = False
        else:
            session = BaseSession(key=key, **kwargs)
            await self.store.save(session.to_row())
            created = True

        return session, created

    async def save(self, session: BaseSession):
        await self.store.save(session.to_row())

    async def delete_by_key(self, key: Key):
        await self.store.delete_by_key(key)
 