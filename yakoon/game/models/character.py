from dataclasses import dataclass

from yakoon.game.runtime.direction import get_exit_direction_commandset
from yakoon.game.stores.room_store import RoomStore      


@dataclass
class Character:
    id: str = ""
    name: str = ""
    location: str = "" # room_id

    async def move_to(self, session, new_location_id):  
        room = RoomStore.get(new_location_id)
        if room:        
            self.location = new_location_id
            self._update_room_commands(session, room) 
            await session.out(f"Du gehst nach {room.name}.")
            await session.out(await room.render(session))
     
    def _update_room_commands(self, session, room):
        router = session.ctx.router
        router.unregister(session.id)
        router.register(session.id, get_exit_direction_commandset(room))