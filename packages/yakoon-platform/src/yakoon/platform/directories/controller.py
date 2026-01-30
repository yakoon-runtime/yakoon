from yakoon.base.controllers.base import BaseController


class ControllerDirectory:
    """
    Registry interface for routing commands to platform definitions.
    Used by the Engine to remain agnostic of domain structure.
    """

    def __init__(self, controllers: list[BaseController]):
        """
        Defines the interface for a registry that manages all available domain controllers.

        A domain registry is responsible for:
        - Providing access to all registered controllers (e.g. gateway, realm, minddojo)
        - Resolving controllers by their unique ID (used in routing, command dispatch, etc.)

        This interface is typically implemented by the system gateway or platform entrypoint
        to coordinate domain activation, switching, and global command handling.
        """

        self._controllers: dict[str, BaseController] = {}    

        has_gateway, gateway_id = False, None
        for controller in controllers:        
            if controller.id in controllers:
                raise ValueError(f"Duplicate controller names detected: {controller.id}")
            if controller.is_gateway and has_gateway:
                raise ValueError(f"Duplicate gateway controller: {gateway_id.id} / {controller.id}")
            if controller.is_gateway:
                has_gateway = True
                gateway_id = controller.id
            self._controllers[controller.id] = controller

        if not has_gateway:
            raise ValueError(f"No gateway controller found")

    def find_gateway(self) -> BaseController:
        for controller in self._controllers.values():        
            if controller.is_gateway:
                return controller

    def get(self, controller_id: str) -> BaseController:
        """
        Resolves and returns a domain controller by its unique ID.

        Args:
            id (str): The identifier of the domain controller (e.g. 'realm', 'gateway').

        Returns:
            BaseController: The matching controller instance.
        """
        
        return self._controllers.get(controller_id)
    
    def get_all(self) -> list[BaseController]:
        """
        Returns all registered domain controllers.

        Returns:
            list[BaseController]: A list of all available domain controllers.
        """

        return self._controllers.values()

    def has(self, controller_id: str) -> bool:
        """
        Returns true if controller has given id.

        Returns:
            bool: True if controller has given id.
        """

        return bool(self._controllers.get(controller_id, {}))