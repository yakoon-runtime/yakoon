from dataclasses import dataclass, field
from typing import ClassVar

from yakoon.base.models.entity import Entity


@dataclass
class Account(Entity):

    name: str = field(default="")
    password_hash: str = field(default="")
    permissions: list[str] = field(default_factory=lambda: ["system"])
   
    __json_fields__: ClassVar[list[str]] = ["permissions"]

    def validate(self):
        if not self.name.strip():
            raise ValueError("Account name must not be empty.")
        if len(self.name) > 30:
            raise ValueError("Account name too long.") 
        

@dataclass(frozen=True, slots=True)
class AuthResult:
    ok: bool
    account: Account | None = None
    reason: str | None = None