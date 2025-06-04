from contextlib import asynccontextmanager
from dataclasses import Field
import asyncpg
from pypika import Table, Query
from yakoon.models import Key
from typing import Any, Optional
import json

from yakoon.models.namespace import Namespace
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

    async def get_by_key(self, key: Key) -> Optional[dict]:
        q = Query.from_(self.table).select('*').where(
            (self.table.domain == key.namespace.domain) &
            (self.table.bucket == key.namespace.bucket) &
            (self.table.scope == key.namespace.scope) &
            (self.table.id == key.id)
        )
        sql = str(q)
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(sql)
            return dict(row) if row else None

    async def fetch_by_namespace(self, namespace: Namespace, *, limit: int = 100) -> list[dict]:
        q = Query.from_(self.table).select('*').where(
            (self.table.domain == namespace.domain) &
            (self.table.bucket == namespace.bucket) &
            (self.table.scope == namespace.scope)
        )
        q = q.limit(limit)
        sql = str(q)
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql)
            return [dict(row) for row in rows]
            
    async def fetch_by_fields(self, *, namespace: Namespace, limit: int = 100, **fields: Any) -> list[dict]:
        q = Query.from_(self.table).select('*').where(
            (self.table.domain == namespace.domain) &
            (self.table.bucket == namespace.bucket) &
            (self.table.scope == namespace.scope)
        )
        for key, value in fields.items():
            q = q.where(self.table[key] == value)
        q = q.limit(limit)

        sql = str(q)

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql)
            return [dict(row) for row in rows]       

    async def save(self, obj: dict) -> None:
        q = f"""
        INSERT INTO {self.table_name} (domain, bucket, scope, id, data)
        VALUES ($1, $2, $3, $4, $5)
        ON CONFLICT (domain, bucket, scope, id)
        DO UPDATE SET data = EXCLUDED.data;
        """
        async with self.pool.acquire() as conn:
            await conn.execute(q,
                obj["domain"], obj["bucket"], obj["scope"], obj["id"],
                json.dumps(obj)
            )

    async def delete_by_key(self, key: Key) -> None:
        q = Query.from_(self.table).delete().where(
            (self.table.domain == key.namespace.domain) &
            (self.table.bucket == key.namespace.bucket) &
            (self.table.scope == key.namespace.scope) &
            (self.table.id == key.id)
        )
        sql = str(q)
        async with self.pool.acquire() as conn:
            await conn.execute(sql)

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
