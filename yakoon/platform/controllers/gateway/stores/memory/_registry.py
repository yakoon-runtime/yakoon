from yakoon.platform.controllers.gateway.stores.memory.account import InMemoryAccountStore
from yakoon.base.stores.base.registry import StoreRegistry


class MemoryStoreRegistry(StoreRegistry):

    def __init__(self):
        self.accounts = InMemoryAccountStore()

