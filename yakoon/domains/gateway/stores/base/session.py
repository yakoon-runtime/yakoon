from abc import ABC, abstractmethod
from typing import Optional

from yakoon.runtime.models.session import BaseSession


class BaseSessionStore(ABC):

    @abstractmethod
    async def get_by_id(self, session_id: str) -> Optional[BaseSession]:
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