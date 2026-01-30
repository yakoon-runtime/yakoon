
from __future__ import annotations
from typing import TypeVar, cast, Awaitable, Callable

T = TypeVar("T")


class ServiceDirectory:

    def __init__(self):
        self._services: dict[object, object] = {}
        self._factories: dict[object, Callable[[], Awaitable[object]]] = {}

    def register_static(self, key: object, service):
        """
        Registers a service statically for a given type.

        Args:
            key (object): The service key.
            service (object): The ready-to-use service.
        """
        self._services[key] = service

    def register_lazy(self, key: object, factory: Callable[[], Awaitable[object]]):
        """
        Registers a lazy factory to produce a servoce for a given bucket.

        Args:
            key (object): The service key.
            factory (Callable): An async function returning a service instance.
        """
        self._factories[key] = factory

    def get(self, key: type[T]) -> T:
        """
        Retrieves the service for a given key.

        If a static service exists, it's returned.
        If a lazy factory is registered, it is awaited and cached.
        Otherwise, a LookupError is raised.

        Args:
            key (object): The key.

        Returns:
            Service: The service for the given context.
        """
        try:
            if key in self._services:       
                return cast(T, self._services[key])
            if key in self._factories:
                registry = self._factories[key]()
                self._services[key] = registry
                return cast(T,registry)
        except KeyError as e:
            raise KeyError(f"Service not registered for key: {key!r}") from e