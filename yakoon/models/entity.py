from dataclasses import dataclass, asdict
from yakoon.models.namespace import Key

@dataclass
class Entity:
    
    key: Key

    def to_dict(self) -> dict:
        return {**{"key": str(self.key)}, **{k: v for k, v in asdict(self).items() if k != "key"}}

    def to_row(self) -> dict:
        return {
            "domain": self.key.namespace.domain,
            "bucket": self.key.namespace.bucket,
            "scope": self.key.namespace.scope,
            "id": self.key.id,
            **{k: v for k, v in asdict(self).items() if k != "key"}
        }

    @classmethod
    def from_row(cls, row: dict):
        return cls(**row)