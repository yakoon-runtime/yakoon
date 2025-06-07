from yakoon.stores.base.registry import StoreRegistry
from yakoon.stores.memory.shard import InMemoryShardCounterStore
from yakoon.stores.memory.session import InMemorySessionStore


class MemoryStoreRegistry(StoreRegistry):

    def __init__(self):
        self.sessions = InMemorySessionStore()
        self.counters = InMemoryShardCounterStore()
    