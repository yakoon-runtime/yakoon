from yakoon.engines.render.jinja import JinjaEngine
from yakoon.services.auditlog import AuditLogService
from yakoon.services.session import SessionService
from yakoon.domains.gateway.services.registry import PlatformServiceRegistry
from yakoon.domains.gateway.services.account import AccountService
from yakoon.domains.gateway.stores.memory.account import InMemoryAccountStore
from yakoon.domains.gateway.stores.memory.session import InMemorySessionStore
from yakoon.services.render import RendererService


def bind_memory_services() -> PlatformServiceRegistry:
    """
    Returns a ServiceRegistry with in-memory store bindings.
    Used for dev, testing, or temporary platforms.
    """
    return PlatformServiceRegistry(
        audit=AuditLogService(),
        renderer=RendererService(JinjaEngine()),
        sessions=SessionService(InMemorySessionStore()),
        accounts=AccountService(InMemoryAccountStore())
    )
