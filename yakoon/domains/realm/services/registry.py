
from yakoon.domains.realm.services.character import CharacterService
from yakoon.domains.realm.services.namespace import NamespaceService
from yakoon.domains.realm.services.room import RoomService
from yakoon.services.registry import ServiceRegistry


class RealmServiceRegistry(ServiceRegistry):

    spaces: NamespaceService
    rooms: RoomService
    chars: CharacterService

    def __init__(self, spaces, rooms, chars):
        self.spaces = spaces
        self.rooms = rooms
        self.chars = chars