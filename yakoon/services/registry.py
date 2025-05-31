

from yakoon.domains.platform.services.account import AccountService
from yakoon.domains.platform.services.session import SessionService


class ServiceRegistry:
    pass


class SessionServiceRegistry(ServiceRegistry):

    sessions: SessionService  = None
    
    def __init__(self, sessions):
        self.sessions = sessions

class PlatformServiceRegistry(SessionServiceRegistry):

    accounts: AccountService

    def __init__(self, sessions, accounts):
        super().__init__(sessions)
        self.accounts = accounts