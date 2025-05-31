from yakoon.engine.io.output import Output
from yakoon.engine.registry import DomainRegistry
from yakoon.core.domain.controller import BaseController


class Context:

    def __init__(self, engine):
        self.depth = 0
        self._engine = engine
        self._registry: DomainRegistry = engine.registry
        self._controller = None

    @property
    def controller(self) -> BaseController:
        return self._controller 
    
    @property
    def platform(self) -> BaseController:
        return self._registry.system
    
    def bind_controller(self, controller: BaseController):
        self._controller = controller

    async def dispatch(self, session, input_str, io: Output):
        depth = session.ctx.depth + 1
        await self._engine.send(session.id, input_str, io, depth)