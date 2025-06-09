from yakoon.saas.domains.realm.stores.memory.character import InMemoryCharacterStore
from yakoon.saas.domains.realm.stores.memory.room import InMemoryRoomStore
from yakoon.saas.stores.base.registry import StoreRegistry


class MemoryStoreRegistry(StoreRegistry):

    def __init__(self):
        self.chars = InMemoryCharacterStore()
        self.rooms = InMemoryRoomStore()

