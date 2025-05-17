from dataclasses import dataclass, field
from typing import List


@dataclass
class Room:
    id: str = ""
    name: str = ""
    desc: str = ""
    objects: List[str] = field(default_factory=list)  # object IDs
    exits: dict[str, str] = field(default_factory=dict) 

    def render(self) -> str:
        parts = [f"|w{self.name}|n", self.desc]

        if self.exits:
            parts.append(f"|cAusgänge:|n {', '.join(self.exits.keys())}")

        return "\n".join(parts)