
from abc import abstractmethod

from yakoon.mesh.controllers.base import BaseController


class BaseControllerDirectory:
    """
    Defines the interface for a registry that manages all available domain controllers.

    A domain registry is responsible for:
    - Providing access to all registered controllers (e.g. gateway, realm, minddojo)
    - Resolving controllers by their unique ID (used in routing, command dispatch, etc.)

    This interface is typically implemented by the system gateway or platform entrypoint
    to coordinate domain activation, switching, and global command handling.
    """

    @abstractmethod
    def get_controllers(self, tanent_id: str) -> list[BaseController]:
        """
        Returns all registered domain controllers.

        Returns:
            list[BaseController]: A list of all available domain controllers.
        """
        ...

    @abstractmethod
    def get_controller_by_id(self, tanent_id: str, id: str) -> BaseController:
        """
        Resolves and returns a domain controller by its unique ID.

        Args:
            id (str): The identifier of the domain controller (e.g. 'realm', 'gateway').

        Returns:
            BaseController: The matching controller instance.
        """
        ...
