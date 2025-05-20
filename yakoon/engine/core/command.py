
from abc import ABC, abstractmethod
from typing import Any


class Command(ABC):
    
    key: str
    aliases: list[str] = []
   
    @abstractmethod
    async def run(self, session: Any, request: Any) -> None:
        pass
    