
from typing import Optional

from yakoon.stores.sqlite.base_store import SQLiteStore


class SQLiteCounterStore(SQLiteStore):
    
    def __init__(self, db_path: str):
        super().__init__(db_path=db_path, table_name="counter_shards")

    async def increment_and_get(self, key: str) -> int:
        q = f"""
        INSERT INTO {self.table_name} (shard, value)
        VALUES (?, 1)
        ON CONFLICT(shard)
        DO UPDATE SET value = value + 1;
        """
        fetch = f"SELECT value FROM {self.table_name} WHERE shard = ?;"

        async with self._connect() as db:
            await db.execute(q, (key,))
            await db.commit()

            cursor = await db.execute(fetch, (key,))
            row = await cursor.fetchone()
            return row[0]

    async def get_shard_stats(self, prefix: str) -> dict:
        q = f"""
        SELECT shard, value
        FROM {self.table_name}
        WHERE shard LIKE ?
        """
        async with self._connect() as db:
            cursor = await db.execute(q, (f"{prefix}%",))
            rows = await cursor.fetchall()
            return {row[0]: row[1] for row in rows}
