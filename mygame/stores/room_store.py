# services/room_store.py
from mygame.models.room import Room

forest = Room(
    id="forest",
    name="Waldlichtung",
    desc="Zwischen alten Bäumen.",
    exits={"n": "hall", "tür": "hall", "norden": "hall"}
)

hall = Room(
    id="hall",
    name="Große Halle",
    desc="Ein weiter Raum.",
    exits={"s": "forest", "süden": "forest"}
)

ROOMS = {
    "forest": forest,
    "hall": hall,
}

class RoomStore:
    @staticmethod
    def get(room_id: str) -> Room | None:
        return ROOMS.get(room_id)