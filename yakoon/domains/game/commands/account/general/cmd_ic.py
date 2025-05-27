from yakoon.domains.game.behavior import CharacterBehavior
from yakoon.domains.game.runtime.data import RuntimeGameData
from yakoon.engine.core.command import Command
from yakoon.engine.core.parser import Request
from yakoon.domains.game.stores.character_store import CharacterStore
from yakoon.solution.platform.runtime.session import SolutionSession


class CmdIC(Command):

    key = "ic"

    async def run(self, session: SolutionSession, request: Request):
        if not request.args:
            return await session.fail("Wen willst du spielen?")

        char_name = request.args[0]
        char = CharacterStore.get_by_name(char_name)
        if not char:
            return await session.fail(f"Charakter '{char_name}' nicht gefunden.")

        runtime_data: RuntimeGameData = session.data_runtime
        if runtime_data.character and runtime_data.character.id == char.id:
            await session.emit(f"Du bist bereits {char.name}.")
            return

        # store the character to session      
        session.data_storage.set(
            session.ctx.controller.name, "char_id", char.id)
        await session.ctx.sessions.persist(session) 

        CharacterBehavior.attach(char)
        await session.emit(f"Du wirst zu {char.name}.")
        await char.move_to(session, char.location)
    