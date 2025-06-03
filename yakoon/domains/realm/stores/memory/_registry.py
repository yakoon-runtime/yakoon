from yakoon.domains.realm.stores.memory.character import InMemoryCharacterStore
from yakoon.domains.realm.stores.memory.room import InMemoryRoomStore
from yakoon.stores.base.registry import StoreRegistry


class MemoryStoreRegistry(StoreRegistry):

    def __init__(self):
        self.chars = InMemoryCharacterStore()
        self.rooms = InMemoryRoomStore()

