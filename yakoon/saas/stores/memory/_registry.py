from yakoon.mesh.stores.base.registry import StoreRegistry
from yakoon.mesh.stores.memory.shard import InMemoryShardCounterStore
from yakoon.saas.stores.memory.session import InMemorySessionStore


class MemoryStoreRegistry(StoreRegistry):

    def __init__(self):
        self.sessions = InMemorySessionStore()
        self.counters = InMemoryShardCounterStore()
    