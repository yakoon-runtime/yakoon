
from yakoon.domains.gateway.services.account import AccountService
from yakoon.runtime.system.registry import GatewayServiceRegistry


class PlatformServiceRegistry(GatewayServiceRegistry):

    accounts: AccountService

    def __init__(self, audit, renderer, sessions, accounts):
        super().__init__(audit, renderer, sessions)
        self.accounts = accounts