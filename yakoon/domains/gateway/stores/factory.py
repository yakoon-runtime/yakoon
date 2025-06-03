
from yakoon.domains.gateway.stores.memory._registry import MemoryStoreRegistry
from yakoon.stores.base.registry import StoreRegistry


def create_stores(backend: str, *, db_path: str = None, pool=None) -> StoreRegistry:

    if backend == "sqlite":
        raise RuntimeError("sqlite not supported")

    elif backend == "postgres":
        raise RuntimeError("postgres not supported")

    elif backend == "memory":
        return MemoryStoreRegistry()
    else:
        raise ValueError(f"Unknown store backend: {backend}")
