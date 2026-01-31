
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class CommandInfo:
    key: str
    category: str | None = None
    controller_id: str | None = None
    permission_groups: tuple[str, ...] = () # später RBAC


@dataclass(frozen=True, slots=True)
class ControllerInfo:
    id: str
    is_shell: bool = False
    is_activatable: bool = False
    is_global_visible: bool = True
    title: str | None = None
    domain: str | None = None  