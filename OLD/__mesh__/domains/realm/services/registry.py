
from yakoon.platform.domains.realm.services.character import CharacterService
from yakoon.platform.domains.realm.services.room import RoomService
from yakoon.platform.runtime.system.registry import ServiceRegistry


class RealmServiceRegistry(ServiceRegistry):

    rooms: RoomService
    chars: CharacterService

    def __init__(self, rooms, chars):
        self.rooms = rooms
        self.chars = chars