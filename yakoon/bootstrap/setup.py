
from yakoon.runtime.system.router import ServiceRouter
from yakoon.services._registry import SystemServiceRegistry
from yakoon.stores.factory import create_stores


def setup_system(service_router: ServiceRouter, name:str):
    stores = create_stores("memory")
    services = SystemServiceRegistry.from_store_registry(stores)

    service_router.register_static(name, services)
