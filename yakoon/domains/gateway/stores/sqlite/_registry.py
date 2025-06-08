from yakoon.domains.gateway.stores.sqlite.account import SQLiteAccountStore
from yakoon.stores.base.registry import StoreRegistry


class SQLiteStoreRegistry(StoreRegistry):

     def __init__(self, db_path: str):
        self.accounts = SQLiteAccountStore(db_path)

