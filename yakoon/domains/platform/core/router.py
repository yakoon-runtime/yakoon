
from typing import Dict
from yakoon.domains.platform.core.registry import BaseServiceRegistry


class ServiceRouter:
    
    def __init__(self):
        self._registries: Dict[str, BaseServiceRegistry] = {}

    def register(self, bucket: str, registry: BaseServiceRegistry):
        """
        Registers a ServiceRegistry instance for a given bucket (e.g., 'minddojo', 'realm').
        """
        self._registries[bucket] = registry

    def get_registry(self, bucket: str) -> BaseServiceRegistry:
        """
        Returns the ServiceRegistry for the given bucket. Raises KeyError if not found.
        """
        return self._registries[bucket]

    def has_registry(self, bucket: str) -> bool:
        """
        Returns True if a registry is registered for the given bucket.
        """
        return bucket in self._registries
