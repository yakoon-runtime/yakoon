from dataclasses import dataclass


@dataclass(frozen=True)
class Namespace:
    world: str
    owner: str  # e.g. account_id, "system", or group-id

    def key(self, object_id: str) -> str:
        return f"{self.world}:{self.owner}:{object_id}"