
from yakoon.saas.domains.realm.models.room import Room
from yakoon.mesh.models.namespace import Namespace

class InMemoryRoomStore:

    def __init__(self):
        self._rooms: dict[str, Room] = {}
        load_defaults(self)

    async def create(self, ns: Namespace, room: Room):
        room.validate()
        self._rooms[ns.get_key(room.id)] = room

    async def get_by_id(self, ns: Namespace, id_: str) -> Room | None:
        return self._rooms.get(ns.get_key(id_))

    async def get_by_name(self, ns: Namespace, name: str) -> Room:
        for k, v, in self._rooms.items():
            if name and name.lower() == v.name.lower():
                return v

    def add(self, ns: Namespace, room: Room):
        room.validate()
        self._rooms[ns.get_key(room.id)] = room


def load_defaults(store: InMemoryRoomStore):

    ns = Namespace(domain="yakoon", bucket="bucket", scope="develop")

    store.add(ns, Room(
        id="forest",
        name="Waldlichtung",
        desc="Zwischen alten Bäumen.",
        exits={"n": "hall", "tür": "hall", "norden": "hall"},
    ))

    store.add(ns, Room(
        id="hall",
        name="Große Halle",
        desc="Ein weiter Raum.",
        exits={"s": "forest", "süden": "forest"},
    ))
