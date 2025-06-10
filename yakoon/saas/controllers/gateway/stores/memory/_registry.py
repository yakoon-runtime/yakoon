from yakoon.saas.controllers.gateway.stores.memory.account import InMemoryAccountStore
from yakoon.mesh.stores.base.registry import StoreRegistry


class MemoryStoreRegistry(StoreRegistry):

    def __init__(self):
        self.accounts = InMemoryAccountStore()

