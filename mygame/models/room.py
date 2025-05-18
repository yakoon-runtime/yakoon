from typing import List
from dataclasses import dataclass, field
from engine.runtime.session import Session


@dataclass
class Room:
    id: str = ""
    name: str = ""
    desc: str = ""
    exits: dict[str, str] = field(default_factory=dict) 

    async def render(self, session:Session) -> str:
        parts = [f"|w{self.name}|n", self.desc]

        objects = session.ctx.game.object_store.contents_of(self.id)
        if objects:
            parts.append(f"└─ Objekte: {', '.join(o.name for o in objects)}")

        if self.exits:
            parts.append(f"└─ Ausgänge: {', '.join(self.exits.keys())}")

        return "\n".join(parts)