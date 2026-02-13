from dataclasses import dataclass, field
from typing import Dict, Optional, Any
from enum import StrEnum

from yakoon.base.models.mode import InteractionMode


class WorkflowContextRequired(Exception):
    pass


@dataclass(frozen=True)
class PromptDef:
    kind: str
    title: str
    var: Optional[str] = None
    required: bool = True

    # nur für select:
    options: list[dict[str, Any]] = field(default_factory=list)

    # optionaler Default (v1: nur select sinnvoll)
    default: Optional[Any] = None


@dataclass(frozen=True)
class SwitchDef:
    expr: str
    cases: dict[str, str] = field(default_factory=dict)
    default: str | None = None


@dataclass(frozen=True)
class StepDef:
    id: str
    run: str | None = None
    prompt: PromptDef | None = None
    next: str | None = None
    branch: dict[str, str] | None = None
    switch: SwitchDef | None = None  # <— neu
    end: str | None = None


@dataclass(frozen=True)
class WorkflowDef:
    id: str
    start: str
    steps: dict[str, StepDef]


@dataclass
class WorkflowError:
    code: str  # PERMISSION_DENIED, COMMAND_FAILED, ...
    message: str
    step_id: str
    command: str | None = None


class WorkflowStatus(StrEnum):
    PREPARED = "prepard"
    RUNNING = "running"
    FAILED = "failed"
    CANCELLED = "cancelled"
    DONE = "done"


@dataclass
class WorkflowBatch:
    batch_id: str
    interaction_mode: InteractionMode
    controller_id: str | None = None

    workflow_id: Optional[str] = None
    values: Dict[str, Any] = field(default_factory=dict)

    current_step: Optional[str] = None
    pending_step: Optional[str] = None

    status: WorkflowStatus = WorkflowStatus.RUNNING
    error: WorkflowError | None = None


@dataclass
class WorkflowRuntime:

    batches: Dict[str, WorkflowBatch] = field(default_factory=dict)

    def get(self, batch_id: str) -> Optional[WorkflowBatch]:
        return self.batches.get(batch_id)

    def ensure(self, batch_id: str, *, interaction_mode: Any) -> WorkflowBatch:
        b = self.batches.get(batch_id)
        if b is None:
            b = WorkflowBatch(batch_id=batch_id, interaction_mode=interaction_mode)
            self.batches[batch_id] = b
        return b

    def remove(self, batch_id: str) -> None:
        self.batches.pop(batch_id, None)
