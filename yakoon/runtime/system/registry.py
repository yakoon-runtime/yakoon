

from abc import abstractmethod


class ServiceRegistry:

    def __init__(self, **services):
        for k, v in services.items():
            setattr(self, k, v)

    @classmethod
    @abstractmethod
    def from_store_registry(cls, stores) -> "ServiceRegistry":
        ...
