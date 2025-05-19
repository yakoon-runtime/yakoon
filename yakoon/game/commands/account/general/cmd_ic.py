from yakoon.engine.core.command import Command
from yakoon.engine.core.parser import Request
from yakoon.game.runtime.session import GameSession
from yakoon.game.stores.character_store import CharacterStore


class CmdIC(Command):

    key = "ic"

    async def run(self, session: GameSession, request: Request):
        if not request.args:
            return await session.err("Wen willst du spielen?")

        char_id = request.args[0]
        char = CharacterStore.get(char_id)
        if session.character and char.id == session.character.id:
            await session.out(f"Du bist bereits {char.name}.")
            return

        if not char:
            return await session.err(f"Charakter '{char_id}' nicht gefunden.")

        session.character = char
        session.command_groups = ["character", session.id]
        await session.out(f"Du wirst zu {char.name}.")
        await session.character.move_to(session, char.location)
    