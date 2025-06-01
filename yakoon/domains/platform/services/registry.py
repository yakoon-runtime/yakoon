
from yakoon.domains.platform.services.account import AccountService
from yakoon.services.registry import GatewayServiceRegistry


class PlatformServiceRegistry(GatewayServiceRegistry):

    accounts: AccountService

    def __init__(self, renderer, sessions, accounts):
        super().__init__(renderer, sessions)
        self.accounts = accounts