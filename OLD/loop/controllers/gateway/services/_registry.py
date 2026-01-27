
from yakoon.base.runtime.system.registry import ServiceRegistry


class GatewayServiceRegistry(ServiceRegistry):

    @classmethod
    def from_store_registry(cls, stores):
        return cls(
            
        )