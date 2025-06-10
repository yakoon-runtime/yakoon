from yakoon.saas.controllers.gateway.stores.sqlite.account import SQLiteAccountStore
from yakoon.mesh.stores.base.registry import StoreRegistry


class SQLiteStoreRegistry(StoreRegistry):

     def __init__(self, db_path: str):
        self.accounts = SQLiteAccountStore(db_path)

