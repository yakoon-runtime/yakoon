from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Mapping, Sequence
from enum import StrEnum
from typing import Any, Protocol, TypeAlias

from yakoon.base.models.account import Account, AuthResult
from yakoon.base.models.catalog import CommandInfo, ControllerInfo
from yakoon.base.models.command import CommandKind
from yakoon.base.models.fields import FieldSpec, FormSpec
from yakoon.base.models.input import DispatchInput
from yakoon.base.models.key import Key
from yakoon.base.models.ns import Namespace
from yakoon.base.models.policy import PolicyValidationError, PolicyValidationResult
from yakoon.base.models.workflow import WorkflowDef, WorkflowRuntime
from yakoon.base.runtime.session.session import Session


class FieldSpecRenderService(Protocol):
    async def build(
        self,
        ctx,
        *,
        section_key: str,
        policy: str,
        **data,
    ) -> FieldSpec: ...


class PolicyService(Protocol):
    def register_field(self, spec: FieldSpec) -> None: ...
    def register_fields(self, specs: list[FieldSpec]) -> None: ...
    def register_defaults(self) -> None: ...
    def get_field(self, key: str) -> FieldSpec: ...
    def validate_field(
        self, *, field: FieldSpec, raw: object
    ) -> PolicyValidationResult: ...
    def validate_form(
        self, *, spec: FormSpec, raw_values: dict[str, object]
    ) -> tuple[dict[str, object], list[PolicyValidationError]]: ...


class WorkflowService(Protocol):
    def runtime(self, session: Any) -> WorkflowRuntime: ...

    def enqueue_next(self, session: Any, batch_id: str) -> None: ...
    def complete_prompt_step(
        self, session: Any, *, batch_id: str, step_id: str, value: Any
    ) -> None: ...
    def complete_run_step(
        self, session: Any, *, batch_id: str, step_id: str
    ) -> None: ...

    def set_value(self, session: Any, batch_id: str, key: str, value: Any) -> None: ...
    def get_def(self, controller_id: str, workflow_key: str) -> Any: ...
    def get_step(self, session: Any, batch_id: str, step_id: str) -> Any: ...

    def fail_batch(
        self,
        session,
        *,
        batch_id: str,
        code: str,
        message: str,
        command: str | None = None,
    ) -> None: ...
    def cancel_batch(self, session, *, batch_id: str) -> None: ...

    def start(
        self,
        session,
        controller_id: str,
        workflow_key: str,
        *,
        enqueue_first: bool = True,
    ) -> str: ...
    def start_with_values(
        self,
        session,
        controller_id: str,
        workflow_key: str,
        values: Mapping[str, Any],
        *,
        enqueue_first: bool = True,
        ignore_none: bool = True,
    ) -> str: ...
    def resume_with_values(
        self,
        session,
        batch_id: str,
        values: Mapping[str, Any],
        *,
        ignore_none: bool = True,
        enqueue_next: bool = True,
    ) -> None: ...


class WorkflowCompileService(Protocol):
    def load_def(self, source: Any, workflow_key: str) -> WorkflowDef: ...


class DialogState(StrEnum):
    IDLE = "idle"
    WAITING_WIZARD = "waiting_wizard"
    WAITING_FORM = "waiting_form"


FieldValue = object
FormValues: TypeAlias = dict[str, object]
DialogValue: TypeAlias = FieldSpec | FormValues


class InputService(Protocol):

    async def ask_field(self, session: Session, field: FieldSpec) -> object: ...
    async def confirm(self, session: Session, field: FieldSpec) -> bool: ...
    async def choice_value(
        self,
        session: Session,
        field: FieldSpec,
        options: list[dict],
        *,
        default: str | None = None,
    ) -> str: ...

    async def choice_index(
        self, session: Session, field: FieldSpec, options: list[str]
    ) -> int: ...


class DialogService(Protocol):

    # lifecycle
    def cleanup(self, session: Session) -> None: ...

    # state
    def state(self, session: Session) -> DialogState: ...
    def is_waiting(self, session: Session) -> bool: ...
    def edge_event(self, session: Session) -> asyncio.Event: ...

    # resolution / cancellation
    def resolve_input(self, session: Session, value: DialogValue) -> bool: ...
    def cancel_input(self, session: Session) -> None: ...

    # wizard (single field)
    def get_field_spec(self, session: Session) -> FieldSpec: ...

    def wait_field(
        self,
        session: Session,
        *,
        field: FieldSpec,
        timeout: float | None = None,
        on_timeout: Callable[[], Awaitable[None]] | None = None,
    ) -> asyncio.Future: ...

    # form (multiple fields)
    def get_form_spec(self, session: Session) -> FormSpec: ...
    def wait_form(
        self,
        session: Session,
        *,
        spec: FormSpec,
        timeout: float | None = None,
        on_timeout: Callable[[], Awaitable[None]] | None = None,
    ) -> asyncio.Future: ...


class CommandQueueService(Protocol):
    def enqueue_commands(self, session, cmds: list[str]) -> None: ...
    def cancel_batch(self, session, batch_id: str) -> None: ...
    def next_input(self, session) -> DispatchInput | None: ...
    def has_pending(self, session) -> bool: ...


class SecretVerifier(Protocol):
    def verify(self, account: Account, secret: str) -> bool: ...


class AuthenticationService(Protocol):
    async def authenticate(
        self, namespace: Namespace, username: str, secret: str
    ) -> AuthResult: ...


class PermissionService(Protocol):

    def register_role(self, name: str, specs: list[str]) -> None: ...
    def set_bootstrap_permissions(self, session: Session): ...
    def apply_account_permissions(self, session: Session, account: Account): ...
    def can_execute(self, session: Session, perm_key: str) -> bool: ...
    def can_read(self, session: Session, perm_key: str) -> bool: ...


class AccountService(Protocol):

    async def get_by_key(self, key: Key) -> Account | None: ...
    async def get_by_username(
        self, namespace: Namespace, name: str
    ) -> Account | None: ...
    async def save(self, account: Account): ...
    async def delete_by_key(self, key: Key): ...


class CommandCatalogService(Protocol):
    def for_controller(self, controller_id: str) -> Sequence[CommandInfo]: ...
    def for_controller_visible(
        self, controller_id: str, session: Session
    ) -> Sequence[CommandInfo]: ...
    def for_man_entries(
        self,
        controller_id: str,
        session: Session,
        mode: str,
        kind_filter: CommandKind | None = None,
    ): ...
    def keys_for_controller(self, controller_id: str) -> Sequence[str]: ...
    def is_shell_builtin(self, key: str) -> bool: ...
    def shell_builtins(self) -> Sequence[str]: ...


class ControllerCatalogService(Protocol):
    def ids(self) -> Sequence[str]: ...
    def all(self) -> Sequence[ControllerInfo]: ...
    def get(self, controller_id: str) -> ControllerInfo | None: ...
    def exists(self, controller_id: str) -> bool: ...
    def activatable(self) -> Sequence[ControllerInfo]: ...
    def listed(self) -> Sequence[ControllerInfo]: ...
    def shell(self) -> Sequence[ControllerInfo]: ...
    def is_shell(self, controller_id: str) -> bool: ...
    def is_activatable(self, controller_id: str) -> bool: ...
    def is_listed(self, controller_id: str) -> bool: ...


class ShardedCounterService(Protocol):
    async def next(self, prefix: str) -> str: ...


class SessionService(Protocol):
    async def delete_by_key(self, key: Key): ...
    async def get(self, key: Key) -> Session: ...
    async def get_or_create(self, key: Key, **kwargs) -> tuple[Session, bool]: ...
    async def save(self, session: Session) -> None: ...

    def release(self, key: Key) -> None: ...
    def clear(self) -> None: ...


class RendererService(Protocol):
    async def render(self, ctx, key: str, **data) -> str: ...


class NamespaceService(Protocol):
    async def from_session(self, session: Session) -> Namespace: ...
    async def get_by_bucket(
        self, bucket: str = "bucket", scope: str = "develop"
    ) -> Namespace: ...


class AuditLogService(Protocol):
    async def audit(self, msg: str): ...
    async def error(self, exc: Exception): ...
    async def permission(self, session, obj, action): ...


class PresenterPrompts(Protocol):

    async def ask(
        self, section_key: str, *, policy: str = "system:string", **data
    ) -> str: ...
    async def ask_secret(
        self, section_key: str, *, policy: str = "system:masked", **data
    ) -> str: ...
    async def confirm(
        self, section_key: str, *, policy: str = "system:string", **data
    ) -> bool: ...
    async def choice_value(
        self,
        section_key: str,
        *,
        policy: str = "system:string",
        options: list[dict],
        default: str | None = None,
        **data,
    ) -> str: ...
    async def choice_index(
        self,
        section_key: str,
        *,
        policy: str = "system:string",
        options: list[str],
        **data,
    ) -> int: ...


class Presenter(Protocol):

    prompts: PresenterPrompts

    async def emit(self, section: str, **data) -> None: ...

    """
    Renders and emits a section of the current template via session.emit().

    Used for standard informational output (e.g. success, details, confirmations).

    Args:
        section (str): Template section key (e.g. "success", "info").
        **data: Optional key-value pairs for template variables.
    """

    async def fail(self, section: str, **data) -> None: ...

    """
    Renders and sends a failure message via session.fail().

    Used to communicate errors, invalid inputs, or blocked operations.

    Args:
        section (str): Template section key (e.g. "not_found", "denied").
        **data: Optional key-value pairs for template variables.
    """

    async def notify(self, section: str, **data) -> None: ...

    """
    Renders and sends a passive notification via session.notify().

    Used for non-critical messages, hints or background updates.

    Args:
        section (str): Template section key (e.g. "hint", "auto_saved").
        **data: Optional key-value pairs for template variables.
    """


class PresenterService(Protocol):
    async def create_presenter(
        self, template_prefix: str, template_key: str, session: Session
    ) -> Presenter: ...
