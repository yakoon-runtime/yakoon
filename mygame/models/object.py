from dataclasses import dataclass, field

from engine.runtime.session import Session

@dataclass
class Object:
    id: str = ""
    name: str = ""
    desc: str = ""
    location: str = ""   # ID eines Raums ODER Objekts
    contains: list[str] = field(default_factory=list)
    movable: bool = True

    def render(self, session:Session) -> str:
        return f"|c{self.name}|n\n{self.desc}"