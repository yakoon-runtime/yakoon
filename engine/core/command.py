
from abc import ABC, abstractmethod
from typing import Any

class Command(ABC):
    key: str
    aliases: list[str] = []
    _engine = None # will assigned from router

    @abstractmethod
    async def run(self, session: Any, request: Any) -> None:
        pass
    