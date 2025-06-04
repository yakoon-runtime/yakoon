
from yakoon.domains.realm.behavior import CharacterBehavior
from yakoon.domains.realm.commands.base import RealmCommand
from yakoon.domains.realm.services.room import RoomService
from yakoon.commands.parser import Request
from yakoon.runtime.models.session import BaseSession


class CmdMove(RealmCommand):

    key = "go"
    aliases = ["move"]
    requires_character = True
    template_key = "character/general/cmd_move"

    async def run(self, session: BaseSession, request: Request):
        presenter = await self.get_presenter(session)
        target = request.args[0] if request.args else None
        if not target:
            return await presenter.fail("missing_arg")

        services = await self.get_domain_services()
        ns = await self.get_namespace(session)

        char = session.ctx("realm", "char", persist=False)
        room = await services.rooms.get_by_id(ns, char.location) if char else None
        if not room:
            return await presenter.fail("no_location")

        dest_id = room.exits.get(target)
        if not dest_id:
            return await presenter.fail("invalid_exit", target=target)

        dest_room = await services.rooms.get_by_id(ns, dest_id)
        if not dest_room:
            return await presenter.fail("not_found", dest=dest_id)

        CharacterBehavior.attach(char)
        await char.move_to(session, dest_room.id)