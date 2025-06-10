from __future__ import annotations
from typing import TYPE_CHECKING
from yakoon.mesh.models.key import Key
from yakoon.saas.controllers.base.base import SaasBaseController
from yakoon.mesh.runtime.session import BaseSession

if TYPE_CHECKING:
    from yakoon.saas.controllers.directory import BaseControllerDirectory


class GatewayBaseController(SaasBaseController):
    """
    Special controller that acts as the system entrypoint and command router.

    The gateway is responsible for:
    - Providing global commands (e.g. help, switch, login)
    - Managing access to all available domain controllers via its registry
    - Coordinating session initialization and domain transitions
    """

    controller_directory: BaseControllerDirectory
    """Registry of all available domain controllers.

    Used by commands like 'switch' and 'help' to resolve domain information at runtime.
    This allows the gateway to act as a global dispatcher and facilitator for domain transitions.
    """

    async def on_resolve_session(self, session_key: Key) -> BaseSession:
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

    async def on_gateway_validate(self, session: BaseSession):
        """
        Platform-level pre-send hook, called before request parsing.

        Used to prepare session context (e.g., account, locale, dynamic commands).
        Only invoked if this controller is the registered `system` controller.
        """
        pass

    async def on_gateway_finalize(self, session: BaseSession):
        """
        Platform-level post-send hook, called after command runing.

        Used to cleanup session context (e.g., account, locale, dynamic commands).
        Only invoked if this controller is the registered `system` controller.
        """
        pass