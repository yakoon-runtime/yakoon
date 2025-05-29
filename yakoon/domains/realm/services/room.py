from yakoon.domains.realm.models.room import Room
from yakoon.domains.realm.stores.memory.room import InMemoryRoomStore


class RoomService:

    store = InMemoryRoomStore()

    @classmethod
    def create(cls, room: Room):
        cls.store.add(room)

    @classmethod
    def get_by_id(cls, id_: str) -> Room | None:
        return cls.store.get_by_id(id_)

    @classmethod
    def find_by_name(cls, name: str) -> list[Room]:
        return cls.store.find_by_name(name)
