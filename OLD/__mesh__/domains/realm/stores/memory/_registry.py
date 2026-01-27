from yakoon.platform.domains.realm.stores.memory.character import InMemoryCharacterStore
from yakoon.platform.domains.realm.stores.memory.room import InMemoryRoomStore
from yakoon.base.stores.base.registry import StoreRegistry


class MemoryStoreRegistry(StoreRegistry):

    def __init__(self):
        self.chars = InMemoryCharacterStore()
        self.rooms = InMemoryRoomStore()

