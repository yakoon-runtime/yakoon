
from yakoon.domains.game.runtime.data import RuntimeGameData
from yakoon.engine.core.command import Command
from yakoon.engine.core.parser import Request
from yakoon.domains.game.stores.room_store import RoomStore
from yakoon.solution.platform.runtime.session import SolutionSession

class CmdLook(Command):

    key = "look"
    aliases = ["see"]
    requires_character = True

    async def run(self, session: SolutionSession, request: Request):
        runtime_data: RuntimeGameData = session.data_runtime
        char = runtime_data.character
        room = RoomStore.get_by_id(char.location) if char else None
        if not room:
            return await session.err("Du bist nirgendwo.")

        await session.send_msg(await room.render(session))