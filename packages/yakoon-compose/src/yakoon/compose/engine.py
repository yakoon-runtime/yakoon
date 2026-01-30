from yakoon.base import ports
from yakoon.base.descriptors.template import TemplateSource
from yakoon.base.directories.service import ServiceDirectory
from yakoon.base.stores.base.registry import StoreRegistry

from yakoon.platform.runtime.render.jinja.engine import JinjaEngine
from yakoon.platform.services.auditlog import AuditLogService
from yakoon.platform.services.namespace import NamespaceService
from yakoon.platform.services.presenter import PresenterService
from yakoon.platform.services.render import RendererService
from yakoon.platform.services.shard import ShardAllocator, ShardedCounterService

from yakoon.platform.directories.controller import ControllerDirectory
from yakoon.platform.engines.command.router import CommandDirectory, CommandRouter
from yakoon.platform.services.session import SessionService
from yakoon.platform.engines.command.engine import Engine
from yakoon.platform.stores.factory import create_system_stores


async def compose_engine(controllers: ControllerDirectory) -> Engine:
    
    stores = await _compose_stores()
    commands = _compose_commands(controllers)
    templates = _compose_template_sources(controllers)
    services = _compose_services(stores, templates)

    gateway = controllers.find_gateway()
    gateway.connect_services(services)

    engine = Engine(controllers, services, commands)    
    return engine


def _compose_commands(directory: ControllerDirectory) -> CommandDirectory:

    commands = CommandDirectory()
    for controller in directory.get_all():
        router = CommandRouter()
        for commands_set in controller.commandsets:
            category = getattr(commands_set, "category", "system")
            router.register(f"{controller.id}:{category}", commands_set)
            commands.register(controller.id, router)

    return commands


def _compose_services(stores: StoreRegistry, template_sources: list[TemplateSource]) -> ServiceDirectory:
    
    services = ServiceDirectory()
    
    services.register_static(ports.AuditLogService, AuditLogService())
    services.register_static(ports.NamespaceService, NamespaceService())
    services.register_static(ports.RendererService, RendererService(JinjaEngine(template_sources)))
    services.register_static(ports.ShardedCounterService, ShardedCounterService(ShardAllocator(stores.counters)))
    services.register_static(ports.SessionService, SessionService(stores.sessions)) 
    services.register_static(ports.PresenterService, PresenterService(services))
    return services   


def _compose_template_sources(directory: ControllerDirectory) -> list[TemplateSource]:
    
    template_sources: list[TemplateSource] = [] 

    for controller in directory.get_all():
        template_sources.append(controller.template_source)
 
    return template_sources


async def _compose_stores() -> StoreRegistry:
    
    stores = await create_system_stores("memory", db_path="db/gateway.sqlite3.db")
    return stores
