from dataclasses import dataclass, field

from yakoon.domains.realm.models.secured import Secured
from yakoon.domains.gateway.runtime.session import GatewaySession


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

    async def render(self, session: GatewaySession) -> str:
        return f"|c{self.name}|n\n{self.desc}"