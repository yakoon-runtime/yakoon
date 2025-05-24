from dataclasses import dataclass, field


@dataclass
class Account:
    id: str = ""
    name: str = ""
    cmd_groups: list[str] = field(default_factory=list)