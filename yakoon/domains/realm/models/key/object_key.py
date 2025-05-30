from dataclasses import dataclass
from .namespace import Namespace


@dataclass(frozen=True)
class ObjectKey:
    namespace: Namespace
    type: str       # e.g. "room", "object", "npc"
    id: str         # local ID within type

    def as_str(self) -> str:
        return f"{self.namespace.world}:{self.namespace.owner}:{self.type}:{self.id}"

    def short(self) -> str:
        return f"{self.type}:{self.id}"
