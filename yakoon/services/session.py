from yakoon.runtime.models.data import RuntimeSessionData
from yakoon.runtime.models.session import BaseSession


class SessionService:
    
    def __init__(self, store):
        self.store = store

    async def get_by_id(self, session_id: str) -> BaseSession:
        return await self.store.get_by_id(session_id)

    async def get_or_create(self, session_id: str, **kwargs) -> tuple[BaseSession, bool]:
        session, created = await self.store.get_or_create(session_id, **kwargs)
        session.data_runtime = RuntimeSessionData() # to avoid runtime state leaks
        return session, created

    async def save(self, session: BaseSession):
        await self.store.save(session)

    async def delete_by_id(self, session_id: str):
        await self.store.delete_by_id(session_id)
    

