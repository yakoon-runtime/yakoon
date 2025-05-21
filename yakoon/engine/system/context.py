from yakoon.engine.core.router import CommandRouter
from yakoon.engine.core.domain.definition import DomainDefinition

class Context:

    def __init__(self, engine):
        self._engine = engine

    @property
    def router(self) -> CommandRouter:
        return self._engine.router

    @property
    def definition(self) -> DomainDefinition:
        return self._engine._domain