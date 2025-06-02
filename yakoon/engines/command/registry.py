from typing import Optional
from yakoon.commands.command import Command
from yakoon.controllers.base import BaseController
from yakoon.controllers.base.gateway import GatewayBaseController
from yakoon.controllers.registry import BaseDomainRegistry
from yakoon.runtime.models.session import BaseSession


class DomainRegistry(BaseDomainRegistry):
    """
    Registry interface for routing commands to platform definitions.
    Used by the Engine to remain agnostic of domain structure.
    """

    def __init__(self, controllers: list[BaseController], 
                 gateway: GatewayBaseController):
        self._gateway = gateway
        self._controllers = controllers
        self._gateway.controller_registry = self

        # Check for duplicate controller names
        names = [c.id for c in self.get_controllers()]
        if len(set(names)) != len(names):
            raise ValueError(f"Duplicate controller names detected: {names}")
        
        # set the gatways to the controllers.
        for controller in controllers:
            controller.gateway = gateway

    def get_gateway(self):
        return self._gateway

    def get_controllers(self):
        return [self._gateway] + self._controllers

    def get_controller_by_id(self, id:str) -> BaseController:
        for controller in self.get_controllers():
            if controller.id == id:
                return controller

    def resolve(self, input_str: str, session: BaseSession) -> Optional[tuple[BaseController, Command]]:
        """
        Resolves a command string based on:
        1. Explicit prefix (e.g. office:print)
        2. Current domain (if active)
        3. gateway controller (only if no domain is active)
        """

        # Include the session-local command group for dynamic routing.
        # This allows commands (e.g. exits or context actions) to be registered
        cmd_groups = session.cmd_groups + session.cmd_groups_dynamic
        
        # 1. Prefix (e.g. realm:look, gateway:help)
        if ":" in input_str:
            prefix, rest = input_str.split(":", 1)
            for controller in self.get_controllers():
                if controller.id == prefix:
                    cmd = controller.router.resolve(rest, cmd_groups)
                    if cmd:
                        return controller, cmd

        # 2. Active domain (switch mode)
        if session.domain_id:
            current = self.get_controller_by_id(session.domain_id)
            cmd = current.router.resolve(input_str, cmd_groups)
            if cmd:
                return current, cmd

        # 3. gateway controller (OOC mode only)
        cmd = self._gateway.router.resolve(input_str, cmd_groups)
        if cmd:
            return self._gateway, cmd

        return None

