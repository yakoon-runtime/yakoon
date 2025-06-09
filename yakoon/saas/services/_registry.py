from dataclasses import dataclass
from yakoon.saas.engines.render.jinja.engine import JinjaEngine
from yakoon.saas.runtime.system.registry import ServiceRegistry
from yakoon.saas.services.auditlog import AuditLogService
from yakoon.saas.services.shard import ShardAllocator, ShardedCounterService
from yakoon.saas.services.namespace import NamespaceService
from yakoon.saas.services.render import RendererService
from yakoon.saas.services.session import SessionService


@dataclass
class SystemServiceRegistry(ServiceRegistry):

    audit: AuditLogService = None
    renderer: RendererService = None
    counters: ShardedCounterService = None
    sessions: SessionService = None
    namespaces: NamespaceService = None
    
    @classmethod
    def from_store_registry(cls, stores):       
        registry = cls(
            audit=AuditLogService(),
            namespaces=NamespaceService(),
            renderer=RendererService(JinjaEngine()),
            counters=ShardedCounterService(ShardAllocator(stores.counters)),
            sessions=SessionService(stores.sessions)
        )
        registry.connect()
        return registry
    