
from typing import Protocol
from engine.runtime.session import Session


class SessionServiceProtocol(Protocol):
    def create(self, account, char) -> Session: ...
    def restore_from_db(self, session_id: str) -> Session | None: ...