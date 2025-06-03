
from yakoon.models import Session
from typing import Optional

from yakoon.stores.sqlite.base_store import SQLiteStore

class SQLiteSessionStore(SQLiteStore):
    
    def __init__(self, db_path: str):
        super().__init__(db_path=db_path, table_name="sessions")

    async def get_by_id(self, id: str) -> Optional[Session]:
        row = await super().get_by_id(id)
        return Session.from_row(row) if row else None

    async def save(self, session: Session) -> None:
        await super().save(session.to_row())

    async def delete(self, id: str) -> None:
        await super().delete(id)

    async def fetch_by_fields(self, *, limit: int = 100, **fields) -> list[Session]:
        rows = await super().fetch_by_fields(limit=limit, **fields)
        return [Session.from_row(row) for row in rows]

    async def fetch_active(self, *, limit: int = 100) -> list[Session]:
        return await self.fetch_by_fields(active=True, limit=limit)

    async def get_by_token(self, token: str) -> Optional[Session]:
        sessions = await self.fetch_by_fields(token=token, limit=1)
        return sessions[0] if sessions else None

    async def expire_all(self) -> None:
        # Mark all sessions as inactive or delete them
        sessions = await self.fetch_by_fields()
        for session in sessions:
            session.active = False
            await self.save(session)
