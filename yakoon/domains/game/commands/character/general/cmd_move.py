
from yakoon.domains.game.behavior import CharacterBehavior
from yakoon.domains.game.runtime.data import RuntimeGameData
from yakoon.engine.core.command import Command
from yakoon.engine.core.parser import Request
from yakoon.domains.game.stores.room_store import RoomStore
from yakoon.solution.platform.runtime.session import SolutionSession


class CmdMove(Command):

    key = "go"
    aliases = ["move"]
    requires_character = True

    async def run(self, session: SolutionSession, request: Request):

        target = request.args[0] if request.args else None
        if not target:
            return await session.fail("Wohin willst du gehen?")

        runtime_data: RuntimeGameData = session.data_runtime
        char = runtime_data.character
        room = RoomStore.get_by_id(char.location) if char else None
        if not room:
            return await session.fail("Du bist nirgendwo.")

        dest_id = room.exits.get(target)
        if not dest_id:
            return await session.fail(f"Hier geht es nicht nach '{target}'.")

        dest_room = RoomStore.get_by_id(dest_id)
        if not dest_room:
            return await session.fail(f"Zielraum '{dest_id}' existiert nicht.")

        CharacterBehavior.attach(char)
        await char.move_to(session, dest_room.id)
