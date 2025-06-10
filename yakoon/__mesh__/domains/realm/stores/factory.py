
from yakoon.saas.domains.realm.stores.memory._registry import MemoryStoreRegistry
from yakoon.saas.domains.realm.stores.sqlite._registry import SQLiteStoreRegistry
from yakoon.mesh.stores.base.registry import StoreRegistry


def create_stores(backend: str, *, db_path: str = None, pool=None) -> StoreRegistry:

    if backend == "sqlite":
        return SQLiteStoreRegistry(db_path or "realm.db")
        raise RuntimeError("sqlite not supported")

    elif backend == "postgres":
        raise RuntimeError("postgres not supported")

    elif backend == "memory":
        return MemoryStoreRegistry()
    else:
        raise ValueError(f"Unknown store backend: {backend}")
