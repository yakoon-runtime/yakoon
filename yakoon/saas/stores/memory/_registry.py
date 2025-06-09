from yakoon.saas.stores.base.registry import StoreRegistry
from yakoon.saas.stores.memory.shard import InMemoryShardCounterStore
from yakoon.saas.stores.memory.session import InMemorySessionStore


class MemoryStoreRegistry(StoreRegistry):

    def __init__(self):
        self.sessions = InMemorySessionStore()
        self.counters = InMemoryShardCounterStore()
    