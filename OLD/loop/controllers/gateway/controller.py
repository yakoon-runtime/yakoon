from yakoon.loop.controllers.gateway.commands.system.cmdset import MeshSystemCommands
from yakoon.loop.runtime.commands.command import MeshCommand
from yakoon.loop.runtime.controllers.base.base import BaseController
from yakoon.loop.runtime.models.key import Key
from yakoon.loop.runtime.runtime.session.session import BaseSession


class MeshGatewayController(BaseController):

    id: str = "gateway"
    """Unique identifier used for command prefix resolution (e.g. realm:look, system:help)."""

    default_command_groups = ["system", "account"]     
    """Names of command groups that are automatically active for every session, 
    without requiring explicit permissions."""

    commandsets = [
        MeshSystemCommands,
    ]
    """ The collection of all commands. """

    async def resolve_command(self, key: str) -> MeshCommand | None:
        for cmd_set in self.commandsets:
            for cmd in cmd_set.commands():
                if cmd.key == key:
                    return cmd()
          
    async def on_initialize(self, session: BaseSession):
        """
        Called after the controller has been fully constructed but before any commands are processed.

        Use this hook to perform asynchronous setup tasks such as loading data, initializing services,
        or validating infrastructure state (e.g., ensuring the admin account exists).

        This method is guaranteed to run once before the first engine tick or command dispatch.
        """
        await super().on_initialize(session)

    async def __on_resolve_session(self, session_key: Key) -> BaseSession:
        """
        Resolves the session object for the given request.

        This method decides whether to load an existing session from storage,
        create a new transient session, or reject the request entirely.

        It must not persist the session unless a valid context (e.g. login) has been established.
        The returned session should be usable by the engine but may remain in-memory only.

        Returns:
            BaseSession: a session instance bound to the request lifecycle
        """

    async def on_gateway_validate(self, session: BaseSession):
        """
        Platform-level pre-send hook, called before request parsing.

        Used to prepare session context (e.g., account, locale, dynamic commands).
        Only invoked if this controller is the registered `system` controller.
        """
            
    async def on_before_run_command(self, session: BaseSession, request, command):
        """
        Hook called immediately before a single command is executed.
        Can be used to enforce permissions, inject context, or audit.
        """

    async def on_gateway_finalize(self, session: BaseSession):
        """
        Platform-level post-send hook, called after command runing.

        Used to cleanup session context (e.g., account, locale, dynamic commands).
        Only invoked if this controller is the registered `gateway` controller.
        """
