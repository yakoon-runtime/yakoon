from __future__ import annotations
from typing import TypeVar, cast, Awaitable, Callable

T = TypeVar("T")


class ServiceDirectory:

    def __init__(
        self, parent: "ServiceDirectory|None" = None, allow_override: bool = False
    ):
        self._parent = parent
        self._allow_override = allow_override
        self._services: dict[object, object] = {}
        self._factories: dict[object, Callable[[], Awaitable[object]]] = {}

    def register_static(self, key: object, service):
        """
        Registers a service statically for a given type.

        Args:
            key (object): The service key.
            service (object): The ready-to-use service.
        """
        if isinstance(service, type):
            raise TypeError("Expected instance, got class. Did you forget ()?")

        if not self._allow_override and self._parent and self._parent.contains(key):
            raise ValueError(f"Service override not allowed: {key}")

        self._services[key] = service

    def register_lazy(self, key: object, factory: Callable[[], Awaitable[object]]):
        """
        Registers a lazy factory to produce a servoce for a given bucket.

        Args:
            key (object): The service key.
            factory (Callable): An async function returning a service instance.
        """
        if not self._allow_override and self._parent and self._parent.contains(key):
            raise ValueError(f"Service override not allowed: {key}")

        self._factories[key] = factory

    def contains(self, key: object) -> bool:
        return key in self._services or (
            self._parent.contains(key) if self._parent else False
        )

    def fork(self, allow_override: bool = False) -> "ServiceDirectory":
        return ServiceDirectory(parent=self, allow_override=allow_override)

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
                return cast(T, registry)
            if self._parent:
                return self._parent.get(key)
            raise KeyError(key)
        except KeyError as e:
            raise KeyError(f"Service not registered for key: {key!r}") from e
