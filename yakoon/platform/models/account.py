from dataclasses import dataclass, field


@dataclass
class Account:
    id: str = ""
    name: str = ""
    cmd_groups: list[str] = field(default_factory=list)

    def validate(self):
        if not self.name.strip():
            raise ValueError("Account name must not be empty.")
        if len(self.name) > 30:
            raise ValueError("Account name too long.")