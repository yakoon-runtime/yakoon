from dataclasses import dataclass
from typing import Callable, Optional

from yakoon.models.entity import Entity
from yakoon.runtime.models.session import BaseSession


@dataclass #(frozen=True, kw_only=True, slots=True)
class Character(Entity):

    name: str = ""
    location: str = "" # room_id

    # THis two field were set by attach().
    on_load_room: Optional[Callable[[str], "Room"]] = None
    on_store_character: Optional[Callable[["Character"], None]] = None

    def validate(self):
        if len(self.name) > 50:
            pass
            #raise DomainValidationError("Room name too long.")

    #__post_init__ 

    async def move_to(self, session: BaseSession, new_location_id):  
        """
        Moves the character to a new room by ID.

        Updates internal location, persists the character state,
        and sends appropriate output to the session (description, feedback).
        """
        print("TODO: move_to")
        return
        room = self.on_load_room(new_location_id)        
        if not room:
            await session.fail("Dieser Ort existiert nicht.")
            return

        self.location = new_location_id
        self.on_store_character(self)

        await session.emit(f"Du gehst in Richtung {room.name}.")
        await session.emit(await room.render(session))
     
