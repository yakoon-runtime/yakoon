from typing import List
from dataclasses import dataclass, field
from yakoon.domains.realm.models.secured import Secured
from yakoon.domains.realm.services.object import ObjectService
from yakoon.platform.runtime.session import PlatformSession


@dataclass
class Room(Secured):
    id: str = ""
    name: str = ""
    desc: str = ""
    exits: dict[str, str] = field(default_factory=dict) 

    def validate(self):
        if len(self.name) > 30:
            raise ValueError("Room name too long.")

    async def render(self, session: PlatformSession) -> str:
        parts = [f"|w{self.name}|n", self.desc]        
        objects = ObjectService.contents_of(self.id)
        if objects:
            parts.append(f"└─ Objekte: {', '.join(o.name for o in objects)}")

        if self.exits:
            parts.append(f"└─ Ausgänge: {', '.join(self.exits.keys())}")

        return "\n".join(parts)