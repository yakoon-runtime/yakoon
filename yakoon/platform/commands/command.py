
from abc import abstractmethod
from typing import Any

from yakoon.engine.core.command import Command


class PlatformCommand(Command):
    
    requires = []
   
    @abstractmethod
    async def run(self, session: Any, request: Any) -> None:
        pass
    