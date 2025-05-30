
from abc import ABC, abstractmethod
from yakoon.engine.system.session import BaseSession
from yakoon.platform.stores.base.session import BaseSessionStore


class BaseSessionService(ABC):

    store: BaseSessionStore = None

    @classmethod
    def bind_storage(cls, store):
        cls.store = store

    @abstractmethod
    async def get_by_id(self, session_id: str) -> BaseSession:
        ...

    @abstractmethod
    async def get_or_create(self, session_id: str, **kwargs) -> tuple[BaseSession, bool]:
        ...

    @abstractmethod
    async def delete_by_id(self, session_id: str) -> None:
        ...

    @abstractmethod
    async def save(self, session: BaseSession) -> None:
        ...

    @abstractmethod
    async def restore_account(session: BaseSession) -> None:
        ...