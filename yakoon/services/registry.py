

from yakoon.services.core.session import SessionService


class ServiceRegistry:
    pass


class SessionServiceRegistry(ServiceRegistry):

    sessions: SessionService  = None
    
    def __init__(self, sessions):
        self.sessions = sessions
