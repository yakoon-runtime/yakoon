
from engine.core.command import Command
from engine.core.parser import Request
from engine.runtime.session import Session


class CmdMove(Command):
    key = "go"
    aliases = ["move"]

    async def run(self, session: Session, request: Request):

        target = request.args[0] if request.args else None
        if not target:
            return await session.err("Wohin willst du gehen?")

        char = session.character
        room = session.ctx.game.room_store.get(char.location) if char else None
        if not room:
            return await session.err("Du bist nirgendwo.")

        dest_id = room.exits.get(target)
        if not dest_id:
            return await session.err(f"Hier geht es nicht nach '{target}'.")

        dest_room = session.ctx.game.room_store.get(dest_id)
        if not dest_room:
            return await session.err(f"Zielraum '{dest_id}' existiert nicht.")
        await session.character.move_to(session, dest_room.id)
