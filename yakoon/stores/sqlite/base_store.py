import aiosqlite
from contextlib import asynccontextmanager
from pypika import Table, Query, Field
from yakoon.models import Key
from typing import Any, Optional
import json

from yakoon.stores.base.base_store import BaseStore


class SQLiteStore(BaseStore):
    """
    SQLite-based implementation of BaseStore.
    Uses aiosqlite and PyPika for efficient and structured SQL interaction.
    """

    def __init__(self, db_path: str, table_name: str):
        self.db_path = db_path
        self.table = Table(table_name)
        self.table_name = table_name

    async def get_by_id(self, id: str) -> Optional[dict]:
        q = Query.from_(self.table).select('*').where(self.table.id == id)
        sql = str(q)
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(sql) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    async def get_by_key(self, key: Key) -> Optional[dict]:
        return await self.get_by_id(key.to_str())

    async def fetch_by_namespace(self, namespace: str, *, limit: int = 100) -> list[dict]:
        q = Query.from_(self.table).select('*').where(self.table.namespace == namespace)
        q = q.limit(limit)
        sql = str(q)
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(sql) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
            
    async def fetch_by_fields(self, *, limit: int = 100, **fields: Any) -> list[dict]:
        if not fields:
            return []

        q = Query.from_(self.table).select('*')
        q = q.limit(limit)
        for key, value in fields.items():
            q = q.where(self.table[key] == value)

        sql = str(q)

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(sql) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    async def save(self, obj: dict) -> None:
        id = obj['id']
        data = json.dumps(obj)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f"REPLACE INTO {self.table_name} (id, namespace, data) VALUES (?, ?, ?)",
                             (id, obj.get('namespace'), data))
            await db.commit()

    async def delete(self, id: str) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (id,))
            await db.commit()

    @asynccontextmanager
    async def _connect(self):
        db = await aiosqlite.connect(self.db_path)
        db.row_factory = aiosqlite.Row
        try:
            yield db
        finally:
            await db.close()

    @asynccontextmanager
    async def transaction(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("BEGIN")
            try:
                yield db
                await db.commit()
            except Exception:
                await db.rollback()
                raise
