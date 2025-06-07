
from yakoon.stores.base.registry import StoreRegistry


def create_system_stores(backend: str, *, db_path: str = None, pool=None) -> StoreRegistry:

    if backend == "sqlite":
        from yakoon.stores.sqlite._registry import SQLiteStoreRegistry
        return SQLiteStoreRegistry(db_path)

    elif backend == "postgres":
        from yakoon.stores.postgres._registry import PostgresStoreRegistry
        if pool is None:
            raise ValueError("Postgres backend requires a connection pool.")
        return PostgresStoreRegistry(pool)

    elif backend == "memory":
        from yakoon.stores.memory._registry import MemoryStoreRegistry
        return MemoryStoreRegistry()

    else:
        raise ValueError(f"Unknown store backend: {backend}")
