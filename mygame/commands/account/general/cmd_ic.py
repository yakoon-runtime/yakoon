from engine.core.command import Command
from engine.core.parser import Request
from engine.runtime.session import Session


class CmdIC(Command):

    key = "ic"

    async def run(self, session: Session, request: Request):
        if not request.args:
            return await session.err("Wen willst du spielen?")

        char_id = request.args[0]
        char = session.ctx.game.character_store.get(char_id)
        if session.character and char.id == session.character.id:
            await session.out(f"Du bist bereits {char.name}.")
            return

        if not char:
            return await session.err(f"Charakter '{char_id}' nicht gefunden.")

        session.character = char
        await session.out(f"Du wirst zu {char.name}.")
        room = session.ctx.game.room_store.get(char.location)
        if room:
            session.ctx.game.update_room_commands(session, room)
            await session.out(room)
