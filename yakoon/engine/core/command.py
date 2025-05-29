
from abc import ABC, abstractmethod
from typing import Any


class Command(ABC):
    
    key: str
    aliases: list[str] = []
    template_key: str = ""
   
    @abstractmethod
    async def run(self, session: Any, request: Any) -> None:
        pass

    @abstractmethod
    def get_template_path(self) -> str:
        pass