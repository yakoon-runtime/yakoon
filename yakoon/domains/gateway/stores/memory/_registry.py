from yakoon.domains.gateway.stores.memory.account import InMemoryAccountStore
from yakoon.stores.base.registry import StoreRegistry


class MemoryStoreRegistry(StoreRegistry):

    def __init__(self):
        self.accounts = InMemoryAccountStore()

