from typing import Dict
from yakoon.domains.platform.core.registry import BaseServiceRegistry
from yakoon.domains.platform.services.account import AccountService
from yakoon.domains.platform.services.session import SessionService


class PlatformServices(BaseServiceRegistry):

    account: AccountService
    session: SessionService

    def register(self):
        self.account = AccountService(InMemoryAccountStore())
        self.session = SessionService(InMemorySessionStore())

