from engine.core.game.definition import BaseGameDefinition


class GameContext:
    
    def __init__(self, engine):
        self._engine = engine

    @property
    def game(self) -> BaseGameDefinition:
        return self._engine._game

    def update_dynamic_commands(self, session, room=None):
        self._engine.update_dynamic_commands(session, room)

    def is_ic(self, session):
        return session.character is not None
