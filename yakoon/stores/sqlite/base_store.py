import aiosqlite
from contextlib import asynccontextmanager
from pypika import Table, Query, Field
from yakoon.models import Key
from typing import Any, Optional
import json

from yakoon.models.namespace import Namespace
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

    async def get_by_key(self, key: Key) -> Optional[dict]:
        q = Query.from_(self.table).select('*').where(
            (self.table.domain == key.namespace.domain) &
            (self.table.bucket == key.namespace.bucket) &
            (self.table.scope == key.namespace.scope) &
            (self.table.id == key.id)
        )
        sql = str(q)
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(sql) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    async def fetch_by_namespace(self, namespace: Namespace, *, limit: int = 100) -> list[dict]:
        q = Query.from_(self.table).select('*').where(
            (self.table.domain == namespace.domain) &
            (self.table.bucket == namespace.bucket) &
            (self.table.scope == namespace.scope)
        )
        q = q.limit(limit)
        sql = str(q)
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(sql) as cursor:
                rows = await cursor.fetchall()
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

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(sql) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    async def save(self, obj: dict) -> None:
        # Upsert via INSERT ... ON CONFLICT (domain, bucket, scope, id)
        q = f"""
        INSERT INTO {self.table_name} (domain, bucket, scope, id, data)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(domain, bucket, scope, id)
        DO UPDATE SET data = excluded.data;
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(q, (
                obj["domain"], obj["bucket"], obj["scope"], obj["id"],
                json.dumps(obj)
            ))
            await db.commit()

    async def delete_by_key(self, key: Key) -> None:
        q = Query.from_(self.table).delete().where(
            (self.table.domain == key.namespace.domain) &
            (self.table.bucket == key.namespace.bucket) &
            (self.table.scope == key.namespace.scope) &
            (self.table.id == key.id)
        )
        sql = str(q)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(sql)
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
