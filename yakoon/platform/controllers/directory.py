from yakoon.base.controllers.base import BaseController
from yakoon.base.controllers.base.directory import BaseControllerDirectory


class ControllerDirectory(BaseControllerDirectory):
    """
    Registry interface for routing commands to platform definitions.
    Used by the Engine to remain agnostic of domain structure.
    """

    @property
    def gateway(self) -> BaseController:
        return self._gateway

    def __init__(self, controllers: list[BaseController], gateway: BaseController):
        self.controllers: dict[str, BaseController] = {}    
        self._gateway = gateway
        self._gateway.controller_directory = self

        for controller in [gateway] + controllers:        
            controller.gateway = gateway
            if controller.id in self.controllers:
                raise ValueError(f"Duplicate controller names detected: {controller.id}")
            self.controllers[controller.id] = controller

    def get(self, controller_id: str) -> BaseController:
        return self.controllers.get(controller_id)
    
    def get_all_for(self) -> list[BaseController]:
        return self.controllers.values()

    def has(self, controller_id: str) -> bool:
        return controller_id in self.controllers.get(controller_id, {})