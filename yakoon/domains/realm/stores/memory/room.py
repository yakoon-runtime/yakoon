
from yakoon.domains.realm.models.room import Room
from yakoon.domains.realm.models.key.namespace import Namespace


class InMemoryRoomStore:

    def __init__(self):
        self._rooms: dict[str, Room] = {}
        load_defaults(self)

    def _make_key(self, ns: Namespace, id_: str) -> str:
        return f"{ns.world}:{ns.owner}:{id_}"

    async def get_by_id(self, ns: Namespace, id_: str) -> Room | None:
        return self._rooms.get(self._make_key(ns, id_))

    def add(self, ns: Namespace, room: Room):
        room.validate()
        self._rooms[self._make_key(ns, room.id)] = room

    async def find_by_name(self, ns: Namespace, name: str) -> list[Room]:
        return [r for k, r in self._rooms.items()
                if k.startswith(f"{ns.world}:{ns.owner}:") and r.name == name]


def load_defaults(store: InMemoryRoomStore):

    ns = Namespace(world="realm", owner="system")

    store.add(ns, Room(
        id="forest",
        name="Waldlichtung",
        desc="Zwischen alten Bäumen.",
        exits={"n": "hall", "tür": "hall", "norden": "hall"},
        namespace=ns
    ))

    store.add(ns, Room(
        id="hall",
        name="Große Halle",
        desc="Ein weiter Raum.",
        exits={"s": "forest", "süden": "forest"},
        namespace=ns
    ))
