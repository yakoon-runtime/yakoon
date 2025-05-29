
from yakoon.domains.realm.commands.base import RealmCommand
from yakoon.engine.core.parser import Request
from yakoon.domains.realm.stores.room_store import RoomStore
from yakoon.solution.platform.runtime.session import SolutionSession


class CmdLook(RealmCommand):

    key = "look"    
    requires_character = True
    aliases = ["see"]

    template_key = "character/general/cmd_look"

    async def run(self, session: SolutionSession, request: Request):
        presenter = self.get_presenter(session)

        char = session.data_runtime.character
        room = RoomStore.get_by_id(char.location) if char else None
        if not room:
            return await presenter.fail("not_found")

        description = await room.render(session)

        await presenter.emit("show", 
            room=room, 
            description=description,
            character=char
        )