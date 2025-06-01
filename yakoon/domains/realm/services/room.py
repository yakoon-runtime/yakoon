from yakoon.domains.realm.models.key import Namespace
from yakoon.domains.realm.models.room import Room


class RoomService:

    def __init__(self, store):
        self.store = store

    async def create(cls, ns: Namespace, room: Room):
        return await cls.store.create(ns, room)

    async def get_by_id(cls, ns: Namespace, id_: str) -> Room | None:
        return await cls.store.get_by_id(ns, id_)

    async def find_by_name(cls, ns: Namespace, name: str) -> list[Room]:
        return await cls.store.find_by_name(ns, name)
