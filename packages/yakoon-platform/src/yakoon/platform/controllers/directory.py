from yakoon.base.controllers.base import BaseController
from yakoon.base.controllers.directory import BaseControllerDirectory


class ControllerDirectory(BaseControllerDirectory):
    """
    Registry interface for routing commands to platform definitions.
    Used by the Engine to remain agnostic of domain structure.
    """

    def __init__(self, controllers: list[BaseController]):
        self._controllers: dict[str, BaseController] = {}    

        has_gateway, gateway_id = False, None
        for controller in controllers:        
            if controller.id in controllers:
                raise ValueError(f"Duplicate controller names detected: {controller.id}")
            if has_gateway:
                raise ValueError(f"Duplicate gateway controller: {gateway_id.id} / {controller.id}")
            if controller.is_gateway:
                has_gateway = True
                gateway_id = controller.id
            self._controllers[controller.id] = controller

        if not has_gateway:
            raise ValueError(f"No gateway controller found")

    async def get_gateway(self) -> BaseController:
        for controller in self._controllers.values():        
            if controller.is_gateway:
                return controller

    async def get(self, controller_id: str) -> BaseController:
        return self._controllers.get(controller_id)
    
    async def get_all_for(self) -> list[BaseController]:
        return self._controllers.values()

    async def has(self, controller_id: str) -> bool:
        return bool(self._controllers.get(controller_id, {}))