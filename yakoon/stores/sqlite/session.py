
from typing import Optional
from yakoon.stores.sqlite.base_store import SQLiteStore


class SQLiteSessionStore(SQLiteStore):

    def __init__(self, db_path: str):
        super().__init__(db_path=db_path, table_name="sessions")

    async def get_by_id(self, id: str) -> Optional[dict]:
        return await super().get_by_id(id)

    async def save(self, session_dict: dict) -> None:
        await super().save(session_dict)

    async def delete(self, id: str) -> None:
        await super().delete(id)

    async def fetch_by_fields(self, *, limit: int = 100, **fields) -> list[dict]:
        return await super().fetch_by_fields(limit=limit, **fields)

    async def fetch_active(self, *, limit: int = 100) -> list[dict]:
        return await self.fetch_by_fields(active=True, limit=limit)

    async def get_by_token(self, token: str) -> Optional[dict]:
        sessions = await self.fetch_by_fields(token=token, limit=1)
        return sessions[0] if sessions else None

    async def expire_all(self) -> None:
        sessions = await self.fetch_by_fields()
        for session in sessions:
            session["active"] = False
            await self.save(session)
