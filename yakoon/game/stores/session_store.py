
from uuid import uuid4
from yakoon.game.runtime.session import GameSession


class SessionStore:
    
    @classmethod
    def persist(cls, session: GameSession):
        pass

    @classmethod
    def restore(cls, session_id: str) -> GameSession | None:
       pass
