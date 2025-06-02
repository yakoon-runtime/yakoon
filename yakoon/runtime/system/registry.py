from yakoon.services.auditlog import AuditLogService
from yakoon.services.session import SessionService
from yakoon.services.render import RendererService


class ServiceRegistry:
    pass


class SessionServiceRegistry(ServiceRegistry):

    sessions: SessionService = None
    
    def __init__(self, sessions):
        self.sessions = sessions


class GatewayServiceRegistry(SessionServiceRegistry):

    audit: AuditLogService = None
    renderer: RendererService = None

    def __init__(self, audit, renderer, sessions):
        super().__init__(sessions)
        self.audit = audit
        self.renderer = renderer