
from typing import Dict
from yakoon.services.registry import ServiceRegistry


class ServiceRouter:
    
    def __init__(self):
        self._registries: Dict[str, ServiceRegistry] = {}

    def register(self, bucket: str, registry: ServiceRegistry):
        """
        Registers a ServiceRegistry instance for a given bucket (e.g., 'minddojo', 'realm').
        """
        self._registries[bucket] = registry

    def get_registry(self, bucket: str) -> ServiceRegistry:
        """
        Returns the ServiceRegistry for the given bucket. Raises KeyError if not found.
        """
        return self._registries[bucket]

    def has_registry(self, bucket: str) -> bool:
        """
        Returns True if a registry is registered for the given bucket.
        """
        return bucket in self._registries
