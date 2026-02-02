from typing import Optional, Protocol, Sequence

from yakoon.base.models.account import Account, AuthResult
from yakoon.base.models.catalog import CommandInfo, ControllerInfo
from yakoon.base.models.key import Key
from yakoon.base.models.namespace import Namespace
from yakoon.base.runtime.session.session import Session


class SessionCommandQueueService(Protocol):
    def push_front_many(self, session, cmds: list[str]) -> None: ...
    def pop_next(self, session) -> str | None: ...
    def has_next(self, session) -> bool: ...


class SecretVerifier(Protocol):
    def verify(self, account: Account, secret: str) -> bool: ...


class AuthenticationService(Protocol):
    async def authenticate(self, namespace: Namespace, username: str, secret: str) -> AuthResult: ...

    
class AccountService(Protocol):

    async def get_by_key(self, key: Key) -> Optional[Account]: ...
    async def get_by_name(self, namespace: Namespace, name: str) -> Optional[Account]: ...    
    async def save(self, account: Account): ...
    async def delete_by_key(self, key: Key): ...
 

class CommandInvokerService(Protocol):
    """
    Executes commands through the normal engine pipeline.
    Used by meta-commands (e.g. batch, aliases) to invoke other commands
    without bypassing routing, permissions, auditing, or rendering.
    """

    async def invoke_text(self, session, text: str) -> bool:
        """Dispatch a single command line as if entered by the user."""


class CommandCatalogService(Protocol):
    def for_controller(self, controller_id: str) -> Sequence[CommandInfo]: ...
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
    async def save(self, session: Session): ...
    async def delete_by_key(self, key: Key): ...
    async def load(self, key: Key) -> Session: ...
    async def load_or_create(self, key: Key, **kwargs) -> tuple[Session, bool]: ...
    """
    Returns an existing session if found, otherwise returns a new (unsaved) session.
    Does not persist the session automatically.
    """
 
class RendererService(Protocol):
    async def render(self, ctx, key: str, **data) -> str: ...
    

class NamespaceService(Protocol):        
    async def from_session(self, session: Session) -> Namespace: ...
    async def get_by_bucket(self, bucket: str="bucket", scope: str="develop") -> Namespace: ...
    

class AuditLogService(Protocol):
    async def audit(self, msg: str): ...
    async def error(self, exc: Exception): ...
    async def permission(self, session, obj, action): ...


class Prompts(Protocol):

    async def ask(self, section: str, **data) -> str: ...
    """     
    Asks the user for free-text input based on a rendered template section.

    Args:
        section (str): The section key within the template.
        **data: Optional data passed to the template.

    Returns:
        str: The user's input as a string.
    """

    async def ask_secret(session: Session, prompt_text: str) -> str: ...
    """     
    Asks the user for free-text input based on a rendered template section.

    Args:
        section (str): The section key within the template.
        **data: Optional data passed to the template.

    Returns:
        str: The user's input as a string.
    """

    async def confirm(self, section: str, **data) -> bool: ...
    """
    Asks the user for a yes/no confirmation using a template-based prompt.

    Args:
        section (str): The section key within the template.
        **data: Optional data passed to the template.

    Returns:
        bool: True if confirmed, False otherwise.
    """

    async def choice(self, section: str, options: list[str], **data) -> str: ...
    """
    Presents the user with a list of choices and returns the selected value.

    Args:
        section (str): The section key within the template.
        choices (list[str]): List of available options.
        **data: Optional data passed to the template.

    Returns:
        str: The chosen value.
    """        

    async def choice_index(self, section: str, options: list[str], **data) -> str: ...
    """
    Presents the user with a numbered list of choices and returns the selected index.

    Args:
        section (str): The section key within the template.
        choices (list[str]): List of available options.
        **data: Optional data passed to the template.

    Returns:
        int: The index of the selected choice (starting at 0).
    """
        

class Presenter(Protocol):

    prompts: Prompts

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
            self, template_prefix: str, template_key: str, session: Session) -> Presenter: ...

