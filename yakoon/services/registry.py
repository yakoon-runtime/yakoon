from yakoon.services.core.session import SessionService
from yakoon.services.renderer.service import RendererService


class ServiceRegistry:
    pass


class SessionServiceRegistry(ServiceRegistry):

    sessions: SessionService = None
    
    def __init__(self, sessions):
        self.sessions = sessions


class GatewayServiceRegistry(SessionServiceRegistry):

    renderer: RendererService = None

    def __init__(self, renderer, sessions):
        super().__init__(sessions)
        self.renderer = renderer