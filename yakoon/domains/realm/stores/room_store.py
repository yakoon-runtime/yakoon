from yakoon.domains.realm.models.room import Room


class RoomStore:
    _rooms: dict[str, Room] = {}

    @classmethod
    def get_by_id(cls, room_id: str) -> Room | None:
        return cls._rooms.get(room_id)
    
    @classmethod
    def add(cls, obj: Room):
        cls._rooms[obj.id] = obj


RoomStore.add(
    Room(id="id:forest", name="Waldlichtung", desc="Zwischen alten Bäumen.",
    exits={"n": "id:hall", "tür": "id:hall", "norden": "id:hall"}))
RoomStore.add(
    Room(id="id:hall", name="Große Halle", desc="Ein weiter Raum.",
    exits={"s": "id:forest", "süden": "id:forest"}))