from engine.core.router import CommandRouter
from engine.core.game.definition import BaseGameDefinition

class GameContext:

    def __init__(self, engine):
        self._engine = engine

    @property
    def router(self) -> CommandRouter:
        return self._engine.router

    @property
    def game(self) -> BaseGameDefinition:
        return self._engine._game