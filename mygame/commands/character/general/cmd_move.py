
from engine.core.command import Command
from engine.core.parser import Request
from mygame.runtime.session import GameSession
from mygame.stores.room_store import RoomStore

class CmdMove(Command):
    key = "go"
    aliases = ["move"]

    async def run(self, session: GameSession, request: Request):

        target = request.args[0] if request.args else None
        if not target:
            return await session.err("Wohin willst du gehen?")

        char = session.character
        room = RoomStore.get(char.location) if char else None
        if not room:
            return await session.err("Du bist nirgendwo.")

        dest_id = room.exits.get(target)
        if not dest_id:
            return await session.err(f"Hier geht es nicht nach '{target}'.")

        dest_room = RoomStore.get(dest_id)
        if not dest_room:
            return await session.err(f"Zielraum '{dest_id}' existiert nicht.")
        await session.character.move_to(session, dest_room.id)
