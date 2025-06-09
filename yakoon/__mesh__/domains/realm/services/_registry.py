
from yakoon.saas.domains.realm.services.character import CharacterService
from yakoon.saas.domains.realm.services.room import RoomService
from yakoon.saas.runtime.system.registry import ServiceRegistry


class RealmServiceRegistry(ServiceRegistry):
    
    rooms: RoomService = None
    chars: CharacterService = None

    @classmethod
    def from_store_registry(cls, stores):
        return cls(
            rooms=RoomService(stores.rooms),
            chars=CharacterService(stores.chars),
        )


