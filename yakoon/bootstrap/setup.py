
from yakoon.runtime.system.router import ServiceRouter
from yakoon.services._registry import SystemServiceRegistry
from yakoon.stores.factory import create_system_stores


async def setup_system(service_router: ServiceRouter, name:str):
    stores = create_system_stores("sqlite", db_path="db/system.sqlite3.db")
    services = SystemServiceRegistry.from_store_registry(stores)

    service_router.register_static(name, services)
