from dataclasses import dataclass

from yakoon.base.descriptors.template import TemplateSource
from yakoon.base.descriptors.workflow import WorkflowSource
from yakoon.base.models.command import (
    CommandAvailability,
    CommandKind,
    CommandVisibility,
)


@dataclass(frozen=True, slots=True)
class CommandInfo:
    key: str
    kind: CommandKind
    visibility: CommandVisibility
    category: str | None = None
    controller_id: str | None = None
    template_prefix: str = ""
    permission_groups: tuple[str, ...] = ()
    availability: CommandAvailability = CommandAvailability.CONTROLLER


@dataclass(frozen=True, slots=True)
class ControllerInfo:
    id: str
    is_shell: bool = False
    is_activatable: bool = False
    is_listed: bool = True
    template_source: TemplateSource | None = None
    workflow_source: WorkflowSource | None = None
