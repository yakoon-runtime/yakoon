from dataclasses import dataclass


@dataclass(frozen=True)
class Namespace:
    bucket: str
    owner: str  # e.g. account_id, "system", or group-id

    def key(self, object_id: str) -> str:
        return f"{self.bucket}:{self.owner}:{object_id}"