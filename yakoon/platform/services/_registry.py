from dataclasses import dataclass
from yakoon.base.runtime.render.jinja.engine import JinjaEngine
from yakoon.base.runtime.system.registry import ServiceRegistry
from yakoon.base.services.shard import ShardAllocator, ShardedCounterService
from yakoon.base.services.namespace import NamespaceService
from yakoon.base.services.render import RendererService
from yakoon.base.services.auditlog import AuditLogService

from yakoon.platform.services.session import SessionService


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
    