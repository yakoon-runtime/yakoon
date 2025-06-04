from dataclasses import dataclass, asdict, fields
from yakoon.models.namespace import Key


@dataclass
class Entity:

    key: Key

    def to_dict(self) -> dict:
        return {
            "key": str(self.key),
            **{
                k: v for k, v in asdict(self).items()
                if k != "key" and not k.startswith("_")
            }
        }

    def to_row(self) -> dict:
        row = {
            "_domain": self.key.namespace.domain,
            "_bucket": self.key.namespace.bucket,
            "_scope": self.key.namespace.scope,
            "_id": self.key.id,
        }
        for f in fields(self):
            if f.name != "key" and not f.name.startswith("_"):
                row[f.name] = getattr(self, f.name)
        return row

    @classmethod
    def from_row(cls, row: dict):
        try:
            key = Key.from_parts(
                row["_domain"], row["_bucket"], row["_scope"], row["_id"]
            )
        except KeyError as e:
            raise ValueError(f"Missing key field in row: {e}") from e

        data = {k: v for k, v in row.items() if not k.startswith("_")}
        return cls(key=key, **data)