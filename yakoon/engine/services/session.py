
from abc import ABC, abstractmethod
from yakoon.engine.system.session import BaseSession


class BaseSessionService(ABC):

    @abstractmethod
    async def get_by_id(self, session_id: str) -> BaseSession:
        ...

    @abstractmethod
    async def get_or_create(self, session_id: str, **kwargs) -> tuple[BaseSession, bool]:
        ...

    @abstractmethod
    async def delete(self, session_id: str) -> None:
        ...

    @abstractmethod
    async def persist(self, session: BaseSession) -> None:
        ...

    @abstractmethod
    async def restore_account(session: BaseSession) -> None:
        ...