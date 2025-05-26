from dataclasses import dataclass
from typing import Callable, Optional

from yakoon.domains.game.models.room import Room
from yakoon.solution.platform.runtime.session import SolutionSession      


@dataclass
class Character:
    id: str = ""
    name: str = ""
    location: str = "" # room_id

    # THis two field were set by attach().
    on_load_room: Optional[Callable[[str], "Room"]] = None
    on_store_character: Optional[Callable[["Character"], None]] = None

    async def move_to(self, session: SolutionSession, new_location_id):  
        """
        Moves the character to a new room by ID.

        Updates internal location, persists the character state,
        and sends appropriate output to the session (description, feedback).
        """
        room = self.on_load_room(new_location_id)        
        if not room:
            await session.err("Dieser Ort existiert nicht.")
            return

        self.location = new_location_id
        self.on_store_character(self)

        await session.send_msg(f"Du gehst in Richtung {room.name}.")
        await session.send_msg(await room.render(session))
     
