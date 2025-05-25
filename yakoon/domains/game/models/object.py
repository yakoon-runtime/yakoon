from dataclasses import dataclass, field

from yakoon.domains.game.models.secured import Secured
from yakoon.solution.platform.runtime.session import SolutionSession


@dataclass
class Object(Secured):
    id: str = ""
    name: str = ""
    desc: str = ""
    location: str = ""   # ID eines Raums ODER Objekts
    contains: list[str] = field(default_factory=list)
    movable: bool = True

    async def render(self, session: SolutionSession) -> str:
        return f"|c{self.name}|n\n{self.desc}"