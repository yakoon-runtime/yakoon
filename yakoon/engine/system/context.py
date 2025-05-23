from yakoon.engine.core.domain.controller import BaseController
from yakoon.engine.core.registry import DomainRegistry
from yakoon.engine.services.session_service import BaseSessionService

class Context:

    def __init__(self, engine):
        self._engine = engine
        self._registry: DomainRegistry = engine.registry
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

    async def send_cmd(self, session, input_str, out, err):
        depth = session.ctx.depth + 1
        await self._engine.send(session.id, input_str, out, err, depth)