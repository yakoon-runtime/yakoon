from typing import List
from dataclasses import dataclass, field
from mygame.models.secured import Secured
from mygame.runtime.session import GameSession
from mygame.stores.object_store import ObjectStore


@dataclass
class Room(Secured):
    id: str = ""
    name: str = ""
    desc: str = ""
    exits: dict[str, str] = field(default_factory=dict) 

    async def render(self, session: GameSession) -> str:
        parts = [f"|w{self.name}|n", self.desc]

        objects = ObjectStore.contents_of(self.id)
        if objects:
            parts.append(f"└─ Objekte: {', '.join(o.name for o in objects)}")

        if self.exits:
            parts.append(f"└─ Ausgänge: {', '.join(self.exits.keys())}")

        return "\n".join(parts)