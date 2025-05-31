
from yakoon.domains.platform.services.account import AccountService
from yakoon.services.registry import SessionServiceRegistry


class PlatformServiceRegistry(SessionServiceRegistry):

    accounts: AccountService

    def __init__(self, sessions, accounts):
        super().__init__(sessions)
        self.accounts = accounts