
from yakoon.saas.domains.realm.services.character import CharacterService
from yakoon.saas.domains.realm.services.room import RoomService
from yakoon.saas.runtime.system.registry import ServiceRegistry


class RealmServiceRegistry(ServiceRegistry):

    rooms: RoomService
    chars: CharacterService

    def __init__(self, rooms, chars):
        self.rooms = rooms
        self.chars = chars