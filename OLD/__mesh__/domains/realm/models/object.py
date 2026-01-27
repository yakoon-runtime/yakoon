from dataclasses import dataclass, field

from yakoon.platform.domains.realm.models.secured import Secured
from yakoon.base.runtime.session import BaseSession


@dataclass
class Object(Secured):
    id: str = ""
    name: str = ""
    desc: str = ""
    location: str = ""   # ID eines Raums ODER Objekts
    contains: list[str] = field(default_factory=list)
    movable: bool = True

    def validate(self):
        pass

    async def render(self, session: BaseSession) -> str:
        return f"|c{self.name}|n\n{self.desc}"