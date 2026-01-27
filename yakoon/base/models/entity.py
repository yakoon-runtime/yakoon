import json
from dataclasses import dataclass, field, fields
from datetime import datetime, UTC
from yakoon.base.models.key import Key


@dataclass
class Entity:

    key: Key
    scope: str = field(init=False)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

   # Subklassen können überschreiben
    __json_fields__: list[str] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self):
        if self.key:
            self.scope = self.key.to_prefix()

    def to_row(self) -> dict:
        base = {
            "__key__": str(self.key),
            "__scope__": self.scope or self.key.to_prefix(),
            "__created_at__": self.created_at,
        }
        for f in fields(self):
            if f.name in {"key", "scope", "created_at"} or f.name.startswith("_"):
                continue
            value = getattr(self, f.name)
            if f.name in self.__json_fields__ and value is not None:
                value = json.dumps(value)
            base[f.name] = value
        return base

    @classmethod
    def from_row(cls, row: dict):
        def safe_json_load(v):
            try:
                return json.loads(v) if isinstance(v, str) else v
            except Exception:
                return v
        key = Key.from_str(row["__key__"])
        created_at = row.get("__created_at__")
        data = {
            k: safe_json_load(v) if k in getattr(cls, "__json_fields__", []) else v
            for k, v in row.items()
            if k not in {"__key__", "__scope__", "__created_at__"}
        }
        return cls(key=key, created_at=created_at, **data)