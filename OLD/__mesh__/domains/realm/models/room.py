from typing import List
from dataclasses import dataclass, field
from yakoon.platform.domains.realm.models.secured import Secured
from yakoon.platform.domains.realm.services.object import ObjectService
from yakoon.base.runtime.session import BaseSession


@dataclass
class Room(Secured):
    id: str = ""
    name: str = ""
    desc: str = ""
    exits: dict[str, str] = field(default_factory=dict)

    def validate(self):
        if len(self.name) > 30:
            raise ValueError("Room name too long.")
        #if not self.namespace:
        #    raise ValueError("Room must have a namespace.")

    async def render(self, session: BaseSession) -> str:
        parts = [f"|w{self.name}|n", self.desc]        

        #objects = ObjectService.contents_of(self.id)
        #if objects:
        #    parts.append(f"└─ Objekte: {', '.join(o.name for o in objects)}")

        #if self.exits:
        #    parts.append(f"└─ Ausgänge: {', '.join(self.exits.keys())}")

        return "\n".join(parts)