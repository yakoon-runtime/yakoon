
from yakoon.domains.realm.behavior import CharacterBehavior
from yakoon.domains.realm.commands.base import RealmCommand
from yakoon.domains.realm.services.room import RoomService
from yakoon.engine.core.parser import Request
from yakoon.platform.runtime.session import PlatformSession


class CmdMove(RealmCommand):

    key = "go"
    aliases = ["move"]
    requires_character = True
    template_key = "character/general/cmd_move"

    async def run(self, session: PlatformSession, request: Request):
        presenter = self.get_presenter(session)

        target = request.args[0] if request.args else None
        if not target:
            return await presenter.fail("missing_arg")

        char = session.data_runtime.character
        room = RoomService.get_by_id(char.location) if char else None
        if not room:
            return await presenter.fail("no_location")

        dest_id = room.exits.get(target)
        if not dest_id:
            return await presenter.fail("invalid_exit", target=target)

        dest_room = RoomService.get_by_id(dest_id)
        if not dest_room:
            return await presenter.fail("not_found", dest=dest_id)

        CharacterBehavior.attach(char)
        await char.move_to(session, dest_room.id)