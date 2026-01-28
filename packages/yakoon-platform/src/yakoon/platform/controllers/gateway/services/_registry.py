
from yakoon.base.runtime.system.registry import ServiceRegistry
from yakoon.platform.controllers.gateway.services.account import AccountService


class GatewayServiceRegistry(ServiceRegistry):

    accounts: AccountService = None

    @classmethod
    def from_store_registry(cls, stores):
        return cls(
            accounts=AccountService(stores.accounts),
        )