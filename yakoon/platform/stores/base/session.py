from abc import ABC, abstractmethod
from typing import Optional

from yakoon.engine.system.session import BaseSession


class BaseSessionStore(ABC):

    @abstractmethod
    async def get_by_id(self, session_id: str) -> Optional[BaseSession]:
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