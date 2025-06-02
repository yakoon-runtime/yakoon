
from yakoon.domains.realm.commands.base import RealmCommand
from yakoon.domains.realm.services.room import RoomService
from yakoon.commands.parser import Request
from yakoon.domains.gateway.runtime.session import GatewaySession


class CmdLook(RealmCommand):

    key = "look"    
    requires_character = True
    aliases = ["see"]

    template_key = "character/general/cmd_look"

    async def run(self, session: GatewaySession, request: Request):
        presenter = await self.get_presenter(session)
        services = await self.get_domain_services()
        char = session.data_runtime.character

        ns = await services.namespaces.from_session(session)
        room = await services.rooms.get_by_id(ns, char.location) if char else None
        if not room:
            return await presenter.fail("not_found")

        description = await room.render(session)

        await presenter.emit("show", 
            room=room, 
            description=description,
            character=char
        )