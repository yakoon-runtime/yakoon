from yakoon.stores.base.registry import StoreRegistry


class SQLiteStoreRegistry(StoreRegistry):

    def __init__(self):
        self.chars = None  # TODO: call store....
        self.rooms = None  

