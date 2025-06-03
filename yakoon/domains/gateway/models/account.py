from dataclasses import asdict, dataclass, field, fields
from uuid import uuid4


@dataclass
class Account:

   # ───── persistent fields (stored in DB/json) ─────

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default="")
    cmd_groups: list[str] = field(default_factory=list) 

    def validate(self):
        if not self.name.strip():
            raise ValueError("Account name must not be empty.")
        if len(self.name) > 30:
            raise ValueError("Account name too long.")
        
    def to_row(self) -> dict:
        return {
            f.name: getattr(self, f.name)
            for f in fields(self)
            if not f.name.startswith("_")
        }

    @classmethod
    def from_row(cls, row: dict):
        return cls(**row)