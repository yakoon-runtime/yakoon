
from uuid import uuid4
from engine.runtime.session import Session


class SessionStore:
    
    @classmethod
    def persist(cls, session: Session):
        pass

    @classmethod
    def restore(cls, session_id: str) -> Session | None:
       pass
