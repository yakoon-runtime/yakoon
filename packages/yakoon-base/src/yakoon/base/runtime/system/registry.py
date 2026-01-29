

from typing import Awaitable, Callable

class ServiceRegistry:

    def __init__(self):
        self._services: dict[str, object] = {}
        self._factories: dict[str, Callable[[], Awaitable[object]]] = {}

    def register_static(self, bucket: str, service):
        """
        Registers a service statically for a given bucket.

        Args:
            bucket (str): The bucket name (e.g. 'realm', 'minddojo').
            service (object): The ready-to-use service.
        """
        self._services[bucket] = service

    def register_lazy(self, bucket: str, factory: Callable[[], Awaitable[object]]):
        """
        Registers a lazy factory to produce a servoce for a given bucket.

        Args:
            bucket (str): The bucket name.
            factory (Callable): An async function returning a service instance.
        """
        self._factories[bucket] = factory

    async def get(self, bucket: str) -> object:
        """
        Retrieves the service for a given bucket.

        If a static service exists, it's returned.
        If a lazy factory is registered, it is awaited and cached.
        Otherwise, a LookupError is raised.

        Args:
            bucket (str): The bucket name.

        Returns:
            Service: The service for the given context.
        """
        if bucket in self._services:
            return self._services[bucket]

        if bucket in self._factories:
            registry = await self._factories[bucket]()
            self._services[bucket] = registry
            return registry

        raise LookupError(f"No service registered for bucket: {bucket}")
