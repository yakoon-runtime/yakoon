


from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ControllerInfo:
    id: str
    is_shell: bool = False
    is_activatable: bool = False
    is_global_visible: bool = True
    title: str | None = None
    domain: str | None = None  