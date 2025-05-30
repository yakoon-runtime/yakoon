

def bind_active_storage(mode: str = "memory"):
    """
    Binds all services to the selected storage backend.

    Supported modes:
    - "memory": in-memory (non-persistent)
    - "sqlite": local SQLite database via SQLAlchemy
    - "postgres": (planned)
    - "redis": (planned)
    """
    if mode == "memory":
        from yakoon.platform.stores.memory._bindings import bind_memory_storages
        bind_memory_storages()

    elif mode == "sqlite":
        from yakoon.platform.stores.sql._bindings import bind_sql_storages
        bind_sql_storages()

    elif mode == "postgres":
        raise NotImplementedError("PostgreSQL binding not yet implemented")

    elif mode == "redis":
        raise NotImplementedError("Redis binding not yet implemented")

    else:
        raise ValueError(f"Unknown storage mode: '{mode}'")
