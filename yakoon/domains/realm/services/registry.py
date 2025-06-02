
from yakoon.domains.realm.services.character import CharacterService
from yakoon.domains.realm.services.room import RoomService
from yakoon.services.counter import ShardedCounterService
from yakoon.services.namespace import NamespaceService
from yakoon.runtime.system.registry import ServiceRegistry


class RealmServiceRegistry(ServiceRegistry):

    counters: ShardedCounterService
    namespaces: NamespaceService
    rooms: RoomService
    chars: CharacterService

    def __init__(self, counters, namespaces, rooms, chars):
        self.counters = counters,
        self.namespaces = namespaces
        self.rooms = rooms
        self.chars = chars