from __future__ import annotations

from yakoon.controllers.base import BaseController

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from yakoon.controllers.registry import BaseDomainRegistry


class GatewayBaseController(BaseController):
    """
    Special controller that acts as the system entrypoint and command router.

    The gateway is responsible for:
    - Providing global commands (e.g. help, switch, login)
    - Managing access to all available domain controllers via its registry
    - Coordinating session initialization and domain transitions
    """

    controller_registry: BaseDomainRegistry
    """Registry of all available domain controllers.

    Used by commands like 'switch' and 'help' to resolve domain information at runtime.
    This allows the gateway to act as a global dispatcher and facilitator for domain transitions.
    """
