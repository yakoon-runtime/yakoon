from yakoon.domains.realm.services.character import CharacterService
from yakoon.domains.realm.services.namespace import NamespaceService
from yakoon.domains.realm.services.registry import RealmServiceRegistry
from yakoon.domains.realm.services.room import RoomService
from yakoon.domains.realm.stores.memory.character import InMemoryCharacterStore
from yakoon.domains.realm.stores.memory.room import InMemoryRoomStore


def bind_memory_services() -> RealmServiceRegistry:
    """
    Returns a ServiceRegistry with in-memory store bindings.
    Used for dev, testing, or temporary platforms.
    """
    return RealmServiceRegistry(
        spaces=NamespaceService("realm"),
        rooms=RoomService(InMemoryRoomStore()),
        chars=CharacterService(InMemoryCharacterStore())
    )
