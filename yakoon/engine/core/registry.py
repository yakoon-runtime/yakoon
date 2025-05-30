# engine/core/registry.py

from typing import Optional
from yakoon.engine.core.command import Command
from yakoon.engine.core.domain.controller import BaseController
from yakoon.engine.services.base.session import BaseSessionService
from yakoon.engine.models.session import BaseSession


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

        # Check for duplicate controller names
        names = [c.name for c in self.get_controllers()]
        if len(set(names)) != len(names):
            raise ValueError(f"Duplicate controller names detected: {names}")
        
    def get_controller_by_name(self, name:str) -> BaseController:
        for controller in self.get_controllers():
            if controller.name == name:
                return controller

    def get_controllers(self):
        return [self.system] + self.controllers

    def resolve(self, input_str: str, session: BaseSession) -> Optional[tuple[BaseController, Command]]:
        """
        Resolves a command string based on:
        1. Explicit prefix (e.g. office:print)
        2. Current domain (if active)
        3. System controller (only if no domain is active)
        """

        # Include the session-local command group for dynamic routing.
        # This allows commands (e.g. exits or context actions) to be registered
        cmd_groups = session.cmd_groups + session.cmd_groups_dynamic
        
        # 1. Prefix (e.g. realm:look, system:help)
        if ":" in input_str:
            prefix, rest = input_str.split(":", 1)
            for controller in self.get_controllers():
                if controller.name == prefix:
                    cmd = controller.router.resolve(rest, cmd_groups)
                    if cmd:
                        return controller, cmd

        # 2. Active domain (switch mode)
        if session.domain:
            cmd = session.domain.router.resolve(input_str, cmd_groups)
            if cmd:
                return session.domain, cmd

        # 3. System controller (OOC mode only)
        cmd = self.system.router.resolve(input_str, cmd_groups)
        if cmd:
            return self.system, cmd

        return None

