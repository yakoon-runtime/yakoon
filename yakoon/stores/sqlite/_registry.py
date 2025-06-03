
from yakoon.stores.base.registry import StoreRegistry
from yakoon.stores.sqlite.counter import SQLiteCounterStore
from yakoon.stores.sqlite.session import SQLiteSessionStore


class SQLiteStoreRegistry(StoreRegistry):

    def __init__(self, db_path="yakoon.db"):
        self.sessions = SQLiteSessionStore(db_path)
        self.counters = SQLiteCounterStore(db_path)
