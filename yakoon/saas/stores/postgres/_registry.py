from yakoon.saas.stores.base.registry import StoreRegistry


class PostgresStoreRegistry(StoreRegistry):

    def __init__(self, pool):
        self.sessions = None
        self.counters = None
