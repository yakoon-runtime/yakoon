from yakoon.platform.domains.realm.models.room import Room
from yakoon.base.models.namespace import Namespace


class RoomService:

    def __init__(self, store):
        self.store = store

    async def create(self, ns: Namespace, room: Room):
        return await self.store.create(ns, room)

    async def get_by_id(self, ns: Namespace, id_: str) -> Room | None:
        return await self.store.get_by_id(ns, id_)

    async def get_by_name(self, ns: Namespace, name: str) -> list[Room]:
        return await self.store.get_by_name(ns, name)

"""
    async def get_by_key(self, key: Key):
        return self._rooms.get(str(key))

    async def get_by_id(self, namespace: Namespace, id_: str):
        return await self.get_by_key(namespace.get_key(id_))

    async def save(self, key: Key, room):
        self._rooms[str(key)] = room
"""