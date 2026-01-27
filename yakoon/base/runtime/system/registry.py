

from abc import abstractmethod


class ServiceRegistry:

    def __init__(self, **services):
        for k, v in services.items():
            setattr(self, k, v)

    @classmethod
    @abstractmethod
    def from_store_registry(cls, stores) -> "ServiceRegistry":
        ...

    def connect(self):
        for field in self.__dataclass_fields__.values():
            service = getattr(self, field.name)
            if hasattr(service, "set_services"):
                service.set_services(self)