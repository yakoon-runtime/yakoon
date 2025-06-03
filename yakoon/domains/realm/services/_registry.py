
from yakoon.domains.realm.services.character import CharacterService
from yakoon.domains.realm.services.room import RoomService
from yakoon.runtime.system.registry import ServiceRegistry


class RealmServiceRegistry(ServiceRegistry):
    
    rooms: RoomService = None
    chars: CharacterService = None

    @classmethod
    def from_store_registry(cls, stores):
        return cls(
            rooms=RoomService(stores.rooms),
            chars=CharacterService(stores.chars),
        )


