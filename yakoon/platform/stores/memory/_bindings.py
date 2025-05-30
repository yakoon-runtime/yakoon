from yakoon.platform.services.account import AccountService
from yakoon.platform.services.session import SessionService
from yakoon.platform.stores.memory.account import InMemoryAccountStore
from yakoon.platform.stores.memory.session import InMemorySessionStore


def bind_memory_storages():
    """
    Binds all platform services to in-memory storage implementations.

    This setup is typically used for development, testing, or runtime environments
    that do not require persistent storage (e.g. SQLite or PostgreSQL).

    Services will operate entirely in RAM and discard state on shutdown.
    """
    SessionService.bind_storage(InMemorySessionStore())
    AccountService.bind_storage(InMemoryAccountStore())
