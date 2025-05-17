from typing import Protocol
from mygame.models.room import Room

class RoomStoreProtocol(Protocol):
    def get(cls, char_id: str) -> Room: ...
        