from typing import Dict
from yakoon.platform.core.registry import BaseServiceRegistry
from yakoon.platform.services.account import AccountService
from yakoon.platform.services.session import SessionService


class PlatformServices(BaseServiceRegistry):

    account: AccountService
    session: SessionService

    def register(self):
        self.account = AccountService(InMemoryAccountStore())
        self.session = SessionService(InMemorySessionStore())

