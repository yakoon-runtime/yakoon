from typing import Callable, Awaitable
from yakoon.runtime.system.registry import ServiceRegistry


class ServiceRouter:
    """
    Manages access to ServiceRegistries for different buckets (contexts/domains).

    Supports both static and lazy registration:
    - Static: predefined ServiceRegistry instances
    - Lazy: factory functions returning ServiceRegistry via await

    This enables multi-bucket setups, late binding, and async configuration logic.
    """

    def __init__(self):
        self._registries: dict[str, ServiceRegistry] = {}
        self._factories: dict[str, Callable[[], Awaitable[ServiceRegistry]]] = {}

    def register_static(self, bucket: str, registry: ServiceRegistry):
        """
        Registers a ServiceRegistry statically for a given bucket.

        Args:
            bucket (str): The bucket name (e.g. 'realm', 'minddojo').
            registry (ServiceRegistry): The ready-to-use service registry.
        """
        self._registries[bucket] = registry

    def register_lazy(self, bucket: str, factory: Callable[[], Awaitable[ServiceRegistry]]):
        """
        Registers a lazy factory to produce a ServiceRegistry for a given bucket.

        Args:
            bucket (str): The bucket name.
            factory (Callable): An async function returning a ServiceRegistry instance.
        """
        self._factories[bucket] = factory

    async def get_registry(self, bucket: str) -> ServiceRegistry:
        """
        Retrieves the ServiceRegistry for a given bucket.

        If a static registry exists, it's returned.
        If a lazy factory is registered, it is awaited and cached.
        Otherwise, a LookupError is raised.

        Args:
            bucket (str): The bucket name.

        Returns:
            ServiceRegistry: The service bundle for the given context.
        """
        if bucket in self._registries:
            return self._registries[bucket]

        if bucket in self._factories:
            registry = await self._factories[bucket]()
            self._registries[bucket] = registry
            return registry

        raise LookupError(f"No services registered for bucket: {bucket}")
