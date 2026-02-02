
from yakoon.base.controllers.base import BaseController
from yakoon.base.models.key import Key
from yakoon.base.models.namespace import Namespace
from yakoon.base.ports import SessionService
from yakoon.base.descriptors.template import TemplateSource
from yakoon.base.runtime.session import Session

from yakoon.auth.commands.cmdset import AuthSystemCommands


class AuthCoreController(BaseController):

    id: str = "auth"

    is_shell: bool = False
    is_listed: bool = True
    is_activatable: bool = True

    default_command_groups = ["system"]     

    template_source = TemplateSource(
        package="yakoon.auth",
        sub_template_path="core")

    commandsets = [
        AuthSystemCommands]
        
    async def on_initialize(self, session: Session):
        """
        Called after the controller has been fully constructed but before any commands are processed.

        Use this hook to perform asynchronous setup tasks such as loading data, initializing services,
        or validating infrastructure state (e.g., ensuring the admin account exists).

        This method is guaranteed to run once before the first engine tick or command dispatch.
        """
        pass

    async def on_resolve_session(self, session_key: Key) -> Session:
        """
        Resolves the session object for the given request.

        This method decides whether to load an existing session from storage,
        create a new transient session, or reject the request entirely.

        It must not persist the session unless a valid context (e.g. login) has been established.
        The returned session should be usable by the engine but may remain in-memory only.

        Returns:
            BaseSession: a session instance bound to the request lifecycle
        """
        pass

    async def on_shell_validate(self, session: Session):
        """
        Platform-level pre-send hook, called before request parsing.

        Used to prepare session context (e.g., account, locale, dynamic commands).
        Only invoked if this controller is the registered `system` controller.
        """
        session.cmd_groups = ["shell:system", ]
        return

        # builds the commandset for this session
        groups = set()
        registry = await self.get_controller_directory()
        for controller in registry.get_controllers():
            groups.update(controller.get_default_command_groups_with_prefix())
        session.cmd_groups = list(groups)

        def merge(lista: list[str], listb: list[str]) -> list[str]:
            return sorted(list(dict.fromkeys(lista + listb)))
        
        # Middleware-Hook: Session was loaded, Account is missing?
        account_key = session.ctx("gateway", "account_key", persist=True)
        if account_key:
            account = await services.accounts.get_by_key(account_key)
            session.set_ctx("gateway", "account", account, persist=False)
            session.cmd_groups = merge(session.cmd_groups, account.cmd_groups)
            
    async def on_before_run_command(self, session: Session, request, command):
        """
        Hook called immediately before a single command is executed.
        Can be used to enforce permissions, inject context, or audit.
        """
        if required := getattr(command, "requires", []):
            account = session.ctx("gateway", "account", persist=False)
            #if not account or not set(required).issubset(set(account.permissions)):
            #    raise PermissionError(f"Auftrag abgelehnt! Erforderliche Rollen: {', '.join(required)}")

    async def on_shell_finalize(self, session: Session):
        """
        Platform-level post-send hook, called after command runing.

        Used to cleanup session context (e.g., account, locale, dynamic commands).
        Only invoked if this controller is the registered `gateway` controller.
        """
        pass
        #if not session.ctx("gateway", "account_key", persist=True):
        #    sessions = self.services.get(SessionService)
        #    await sessions.delete_by_key(session.key)
