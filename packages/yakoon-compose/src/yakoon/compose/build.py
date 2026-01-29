from yakoon.base.runtime.system.registry import ServiceRegistry
from yakoon.base.runtime.views.template import TemplateSource
from yakoon.base.stores.base.registry import StoreRegistry

from yakoon.platform.runtime.render.jinja.engine import JinjaEngine
from yakoon.platform.services.auditlog import AuditLogService
from yakoon.platform.services.namespace import NamespaceService
from yakoon.platform.services.render import RendererService
from yakoon.platform.services.shard import ShardAllocator, ShardedCounterService

from yakoon.platform.controllers.directory import ControllerDirectory
from yakoon.platform.engines.command.router import CommandDirectory, CommandRouter
from yakoon.platform.services.session import SessionService
from yakoon.platform.engines.command.engine import Engine
from yakoon.platform.stores.factory import create_system_stores


async def compose_engine(controllers: ControllerDirectory) -> Engine:
    
    stores = await _compose_stores()
    commands = await _compose_commands(controllers)
    templates = await _compose_template_sources(controllers)
    services = await _compose_services(stores, templates)

    gateway = await controllers.get_gateway()
    await gateway.connect_services(services)

    engine = Engine(controllers, services, commands)    
    return engine


async def _compose_commands(directory: ControllerDirectory) -> CommandDirectory:

    commands = CommandDirectory()
    for controller in await directory.get_all_for():
        router = CommandRouter()
        for commands_set in controller.commandsets:
            category = getattr(commands_set, "category", "system")
            await router.register(f"{controller.id}:{category}", commands_set)
            await commands.register(controller.id, router)

    return commands


async def _compose_stores() -> StoreRegistry:
    
    stores = await create_system_stores("memory", db_path="db/gateway.sqlite3.db")
    return stores


async def _compose_services(stores: StoreRegistry, template_sources: list[TemplateSource]) -> ServiceRegistry:
    
    services = ServiceRegistry()
    
    services.register_static("audit", AuditLogService())
    services.register_static("namespaces", NamespaceService())
    services.register_static("renderer", RendererService(JinjaEngine(template_sources)))
    services.register_static("counters", ShardedCounterService(ShardAllocator(stores.counters)))
    services.register_static("sessions", SessionService(stores.sessions)) 
    return services   


async def _compose_template_sources(directory: ControllerDirectory) -> list[TemplateSource]:
    
    template_sources: list[TemplateSource] = [] 

    for controller in await directory.get_all_for():
        template_sources.append(controller.template_source)
 
    return template_sources
