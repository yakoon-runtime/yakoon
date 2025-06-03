
from yakoon.domains.gateway.services._registry import GatewayServiceRegistry
from yakoon.domains.gateway.stores.factory import create_stores


def setup_gateway(service_router, name:str):
    stores = create_stores("memory")
    services = GatewayServiceRegistry.from_store_registry(stores)

    service_router.register_static(name, services)
    #await ensure_admin_account(services.accounts)
