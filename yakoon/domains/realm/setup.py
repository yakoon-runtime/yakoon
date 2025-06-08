
from yakoon.domains.realm.services._registry import RealmServiceRegistry
from yakoon.domains.realm.stores.factory import create_stores


async def setup_realm(service_router, name:str):
    stores = create_stores("memory")
    services = RealmServiceRegistry.from_store_registry(stores)

    service_router.register_static(name, services)