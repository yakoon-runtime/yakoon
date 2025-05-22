# yakoon/platform/session_store.py
from abc import ABC, abstractmethod
from typing import Optional

from yakoon.platform.runtime.session import PlatformSession


class SessionStore(ABC):

    @abstractmethod
    async def get_by_id(self, session_id: str) -> Optional[PlatformSession]:
        ...

    @abstractmethod
    async def get_or_create(self, session_id: str, **kwargs) -> tuple[PlatformSession, bool]:
        ...

    @abstractmethod
    async def delete(self, session_id: str) -> None:
        ...

    @abstractmethod
    async def persist(self, session: PlatformSession) -> None:
        ...