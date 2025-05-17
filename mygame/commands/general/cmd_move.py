
from engine.core.command import Command
from engine.core.parser import Request
from engine.runtime.session import Session
from mygame.stores.room_store import RoomStore

class CmdMove(Command):
    key = "go"
    aliases = ["move"]

    async def run(self, session: Session, request: Request):

        target = request.subcmd or (request.args[0] if request.args else None)
        if not target:
            return await session.err("Wohin willst du gehen?")

        char = session.character
        room = RoomStore.get(char.location)
        if not room:
            return await session.err("Du bist nirgendwo.")

        dest_id = room.exits.get(target)
        if not dest_id:
            return await session.err(f"Hier geht es nicht nach '{target}'.")

        room = RoomStore.get(dest_id)
        if not room:
            return await session.err(f"Zielraum '{dest_id}' existiert nicht.")

        char.location = room.id
        await session.out(f"Du gehst nach |w{room.name}|n.")
        await session.out(room.render())