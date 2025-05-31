
from abc import ABC, abstractmethod
from yakoon.runtime.models.session import BaseSession
from yakoon.domains.platform.stores.base.session import BaseSessionStore


class BaseSessionService(ABC):

    store: BaseSessionStore = None

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