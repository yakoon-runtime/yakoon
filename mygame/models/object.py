from dataclasses import dataclass, field

from mygame.models.secured import Secured
from mygame.runtime.session import GameSession


@dataclass
class Object(Secured):
    id: str = ""
    name: str = ""
    desc: str = ""
    location: str = ""   # ID eines Raums ODER Objekts
    contains: list[str] = field(default_factory=list)
    movable: bool = True

    async def render(self, session:GameSession) -> str:
        return f"|c{self.name}|n\n{self.desc}"