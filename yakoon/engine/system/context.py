from yakoon.engine.core.domain.controller import BaseController
from yakoon.engine.core.registry import DomainRegistry
from yakoon.engine.services.session_service import BaseSessionService

class Context:

    def __init__(self, registry: DomainRegistry):
        self._registry = registry
        self._controller = None

    @property
    def controller(self) -> BaseController:
        return self._controller 
    
    @property
    def sessions(self) -> BaseSessionService:
        return self._registry.sessions
    
    @property
    def platform(self) -> BaseController:
        return self._registry.system
    
    def bind_controller(self, controller: BaseController):
        self._controller = controller