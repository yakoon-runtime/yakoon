
from yakoon.saas.controllers.gateway.services.account import AccountService
from yakoon.saas.runtime.system.registry import ServiceRegistry


class GatewayServiceRegistry(ServiceRegistry):

    accounts: AccountService = None

    @classmethod
    def from_store_registry(cls, stores):
        return cls(
            accounts=AccountService(stores.accounts),
        )