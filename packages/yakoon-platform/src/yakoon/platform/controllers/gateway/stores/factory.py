
from yakoon.platform.controllers.gateway.stores.memory._registry import MemoryStoreRegistry
from yakoon.base.stores.base.registry import StoreRegistry


def create_gateway_stores(backend: str, *, db_path: str = None, pool=None) -> StoreRegistry:

    if backend == "sqlite":
        from yakoon.platform.controllers.gateway.stores.sqlite._registry import SQLiteStoreRegistry
        return SQLiteStoreRegistry(db_path)

    elif backend == "postgres":
        raise RuntimeError("postgres not supported")

    elif backend == "memory":
        return MemoryStoreRegistry()
    else:
        raise ValueError(f"Unknown store backend: {backend}")
