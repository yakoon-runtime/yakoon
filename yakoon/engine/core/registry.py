# engine/core/registry.py

from yakoon.engine.core.domain.controller import BaseController
from yakoon.engine.services.session_service import BaseSessionService
from yakoon.engine.system.session import BaseSession


class DomainRegistry:
    """
    Registry interface for routing commands to platform definitions.
    Used by the Engine to remain agnostic of domain structure.
    """

    def __init__(self, controllers: list[BaseController], 
                 system: BaseController, 
                 sessions: BaseSessionService):
        self.system = system
        self.controllers = controllers
        self.sessions = sessions

    def resolve(self, input_str: str, session: BaseSession):
        """
        Try to resolve the command using self or one of the registered domains.
        Returns a tuple of (responsible definition, command) or None.
        """
        for controller in [self.system] + self.controllers:
            cmd = controller.router.resolve(input_str, session.command_groups)
            if cmd:
                return controller, cmd
        return None