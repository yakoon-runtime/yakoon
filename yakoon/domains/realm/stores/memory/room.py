
from yakoon.domains.realm.models import Room


class InMemoryRoomStore:

    def __init__(self):
        self._rooms: dict[str, Room] = {}
        load_defaults(self)
        
    def get_by_id(self, id_: str) -> Room | None:
        return self._rooms.get(id_)

    def add(self, room: Room):
        room.validate()
        self._rooms[room.id] = room

    def find_by_name(self, name: str) -> list[Room]:
        return [r for r in self._rooms.values() if r.name == name]


def load_defaults(store: InMemoryRoomStore):
    store.add(
        Room(id="id:forest", name="Waldlichtung", desc="Zwischen alten Bäumen.",
        exits={"n": "id:hall", "tür": "id:hall", "norden": "id:hall"}))
    store.add(
        Room(id="id:hall", name="Große Halle", desc="Ein weiter Raum.",
        exits={"s": "id:forest", "süden": "id:forest"}))