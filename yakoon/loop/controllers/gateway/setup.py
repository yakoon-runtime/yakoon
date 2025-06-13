
from yakoon.loop.controllers.gateway.services._registry import GatewayServiceRegistry
from yakoon.loop.controllers.gateway.stores.factory import create_gateway_stores


async def setup_gateway(service_router, name:str):
    stores = create_gateway_stores("memory", db_path="db/gateway.sqlite3.db")
    services = GatewayServiceRegistry.from_store_registry(stores)

    service_router.register_static(name, services)
