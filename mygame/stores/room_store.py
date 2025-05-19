from mygame.models.room import Room


class RoomStore:
    _rooms: dict[str, Room] = {}

    @classmethod
    def get(cls, room_id: str) -> Room | None:
        return cls._rooms.get(room_id)
    
    @classmethod
    def put(cls, obj: Room):
        cls._rooms[obj.id] = obj


RoomStore.put(
    Room(id="forest", name="Waldlichtung", desc="Zwischen alten Bäumen.",
    exits={"n": "hall", "tür": "hall", "norden": "hall"}))
RoomStore.put(
    Room(id="hall", name="Große Halle", desc="Ein weiter Raum.",
    exits={"s": "forest", "süden": "forest"}))