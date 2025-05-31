from yakoon.services.core.session import SessionService
from yakoon.domains.platform.services.registry import PlatformServiceRegistry
from yakoon.domains.platform.services.account import AccountService
from yakoon.domains.platform.stores.memory.account import InMemoryAccountStore
from yakoon.domains.platform.stores.memory.session import InMemorySessionStore


def bind_memory_services() -> PlatformServiceRegistry:
    """
    Returns a ServiceRegistry with in-memory store bindings.
    Used for dev, testing, or temporary platforms.
    """
    return PlatformServiceRegistry(
        sessions=SessionService(InMemorySessionStore()),
        accounts=AccountService(InMemoryAccountStore())
    )
