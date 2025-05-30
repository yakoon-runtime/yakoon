from yakoon.domains.realm.models.key import Namespace
from yakoon.domains.realm.models.room import Room
from yakoon.domains.realm.stores.memory.room import InMemoryRoomStore


class RoomService:

    store = InMemoryRoomStore() 

    @classmethod
    async def create(cls, ns: Namespace, room: Room):
        await cls.store.add(ns, room)

    @classmethod
    async def get_by_id(cls, ns: Namespace, id_: str) -> Room | None:
        return await cls.store.get_by_id(ns, id_)

    @classmethod
    async def find_by_name(cls, ns: Namespace, name: str) -> list[Room]:
        return await cls.store.find_by_name(ns, name)
