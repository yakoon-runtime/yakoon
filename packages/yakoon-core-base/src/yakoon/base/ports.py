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
from yakoon.base.models.message import MessageSpec
from yakoon.base.models.ns import Namespace
from yakoon.base.models.policy import (
    FieldPolicy,
    PolicyValidationResult,
    RawValue,
)
from yakoon.base.models.workflow import StepDef, WorkflowDef, WorkflowRuntime
from yakoon.base.runtime.session.session import Session
from yakoon.platform.runtime.render.context import RenderContext


class MessageSpecService(Protocol):

    async def parse_spec(self, yaml_text: str) -> MessageSpec: ...


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
    def register_policy(self, policy: FieldPolicy) -> None: ...
    def register_policies(self, policies: list[FieldPolicy]) -> None: ...
    def get_policy(self, key: str) -> FieldPolicy: ...
    def register_validator(self, key: str, fn) -> None: ...
    def get_validator(self, key: str) -> callable: ...
    def register_defaults(self) -> None: ...
    def validate_field(
        self, *, field: FieldSpec, raw: RawValue
    ) -> PolicyValidationResult: ...
    def materialize_field(
        self,
        policy_key: str,
        *,
        key: str,
        label: str,
        required: bool | None = None,
        hint: str | None = None,
        secret: bool | None = None,
        options: list[dict] | None = None,
        default: object | None = None,
    ) -> FieldSpec: ...


class WorkflowService(Protocol):
    def runtime(self, session: Any) -> WorkflowRuntime: ...

    def enqueue_next(self, session: Any, batch_id: str) -> None: ...
    def complete_input_step(
        self,
        session,
        *,
        batch_id: str,
        step_id: str,
        values: Mapping[str, Any],
        ignore_none: bool = True,
    ) -> None: ...

    def complete_run_step(
        self, session: Any, *, batch_id: str, step_id: str
    ) -> None: ...

    def set_value(self, session: Any, batch_id: str, key: str, value: Any) -> None: ...
    def get_def(self, controller_id: str, command_key: str) -> WorkflowDef: ...
    def get_step(self, session: Any, batch_id: str, step_id: str) -> StepDef: ...

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
        command_key: str,
        *,
        enqueue_first: bool = True,
    ) -> str: ...
    def start_with_values(
        self,
        session,
        controller_id: str,
        command_key: str,
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
    def load_def(self, source: Any, command_key: str) -> WorkflowDef: ...


class DialogState(StrEnum):
    IDLE = "idle"
    WAITING_WIZARD = "waiting_wizard"
    WAITING_FORM = "waiting_form"


FieldValue = object
FormValues: TypeAlias = dict[str, object]
DialogValue: TypeAlias = FieldSpec | FormValues


class InputService(Protocol):

    async def ask_form(self, session: Session, spec: FormSpec) -> dict[str, object]: ...
    async def ask_field(self, session: Session, field: FieldSpec) -> object: ...


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

    # form (multiple fields)
    def get_form_spec(self, session: Session) -> FormSpec: ...
    def wait_input(
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
    async def render_text(self, ctx: RenderContext, key: str, **data) -> str: ...
    async def render_spec(
        self, ctx: RenderContext, key: str, **data
    ) -> MessageSpec: ...


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

    DEFAULT_POLICY = "system:string"
    DEFAULT_MASK_POLICY = "system:masked"

    async def ask(
        self, section_key: str, *, policy: str = DEFAULT_POLICY, **data
    ) -> object: ...

    async def ask_secret(
        self, section_key: str, *, policy: str = DEFAULT_MASK_POLICY, **data
    ) -> object: ...


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
