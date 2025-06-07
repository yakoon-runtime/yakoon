from dataclasses import dataclass, field, fields
from datetime import datetime, UTC
from yakoon.models.key import Key


@dataclass
class Entity:

    key: Key
    scope: str = field(init=False)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def __post_init__(self):
        if self.key:
            self.scope = self.key.to_prefix()

    def to_row(self) -> dict:
        return {
            "key": str(self.key),
            "scope": self.scope or self.key.to_prefix(),
            "created_at": self.created_at,
            **{
                f.name: getattr(self, f.name)
                for f in fields(self)
                if f.name not in {"key", "scope", "created_at"} and not f.name.startswith("_")
            }
        }

    @classmethod
    def from_row(cls, row: dict):
        key = Key.from_str(row["key"])
        created_at = row.get("created_at")

        # alles außer Standardfelder übernehmen
        data = {
            k: v for k, v in row.items()
            if k not in {"key", "scope", "created_at"}
        }
        return cls(key=key, created_at=created_at, **data)