from dataclasses import dataclass, field
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