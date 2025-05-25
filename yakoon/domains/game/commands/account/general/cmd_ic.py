from yakoon.engine.core.command import Command
from yakoon.engine.core.parser import Request
from yakoon.domains.game.stores.character_store import CharacterStore
from yakoon.solution.platform.runtime.session import SolutionSession


class CmdIC(Command):

    key = "ic"

    async def run(self, session: SolutionSession, request: Request):
        if not request.args:
            return await session.err("Wen willst du spielen?")

        char_id = request.args[0]
        char = CharacterStore.get(char_id) # TODO: by name....
        if session.character and char.id == session.character.id:
            await session.out(f"Du bist bereits {char.name}.")
            return

        if not char:
            return await session.err(f"Charakter '{char_id}' nicht gefunden.")

        # store the character to session      
        session.data_storage.set(
            session.ctx.controller.name, "char_id", char.id)
        
        await session.out(f"Du wirst zu {char.name}.")
        await session.character.move_to(session, char.location)
    