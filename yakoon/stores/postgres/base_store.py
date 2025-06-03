from contextlib import asynccontextmanager
from dataclasses import Field
import asyncpg
from pypika import Table, Query
from yakoon.models import Key
from typing import Any, Optional
import json

from yakoon.stores.base.base_store import BaseStore


class PostgresStore(BaseStore):
    """
    PostgreSQL-based implementation of BaseStore.
    Uses asyncpg and PyPika for efficient and structured SQL interaction.
    """

    def __init__(self, pool: asyncpg.Pool, table_name: str):
        self.pool = pool
        self.table = Table(table_name)
        self.table_name = table_name

    async def get_by_id(self, id: str) -> Optional[dict]:
        q = Query.from_(self.table).select('*').where(self.table.id == id)
        sql = str(q)
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(sql)
            return dict(row) if row else None

    async def get_by_key(self, key: Key) -> Optional[dict]:
        return await self.get_by_id(key.to_str())

    async def fetch_by_namespace(self, namespace: str, *, limit: int = 100) -> list[dict]:
        q = Query.from_(self.table).select('*').where(self.table.namespace == namespace)
        q = q.limit(limit)
        sql = str(q)
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql)
            return [dict(row) for row in rows]
            
    async def fetch_by_fields(self, *, limit: int = 100, **fields: Any) -> list[dict]:
        q = Query.from_(self.table).select('*')
        q = q.limit(limit)
        for key, value in fields.items():
            q = q.where(Field(key) == value)
        sql = str(q)
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql)
            return [dict(row) for row in rows]        

    async def save(self, obj: dict) -> None:
        id = obj['id']
        data = json.dumps(obj)
        async with self.pool.acquire() as conn:
            await conn.execute(f"""
                INSERT INTO {self.table_name} (id, namespace, data)
                VALUES ($1, $2, $3)
                ON CONFLICT (id) DO UPDATE
                SET namespace = EXCLUDED.namespace,
                    data = EXCLUDED.data
            """, id, obj.get('namespace'), data)

    async def delete(self, id: str) -> None:
        async with self.pool.acquire() as conn:
            await conn.execute(f"DELETE FROM {self.table_name} WHERE id = $1", id)

    @asynccontextmanager
    async def _acquire(self):
        conn = await self.pool.acquire()
        try:
            yield conn
        finally:
            await self.pool.release(conn)

    @asynccontextmanager
    async def transaction(self):
        conn = await self.pool.acquire()
        tr = conn.transaction()
        await tr.start()
        try:
            yield conn
            await tr.commit()
        except Exception:
            await tr.rollback()
            raise
        finally:
            await self.pool.release(conn)
