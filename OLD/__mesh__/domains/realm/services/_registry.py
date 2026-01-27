
from yakoon.platform.domains.realm.services.character import CharacterService
from yakoon.platform.domains.realm.services.room import RoomService
from yakoon.platform.runtime.system.registry import ServiceRegistry


class RealmServiceRegistry(ServiceRegistry):
    
    rooms: RoomService = None
    chars: CharacterService = None

    @classmethod
    def from_store_registry(cls, stores):
        return cls(
            rooms=RoomService(stores.rooms),
            chars=CharacterService(stores.chars),
        )


