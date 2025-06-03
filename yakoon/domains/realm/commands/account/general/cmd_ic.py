from yakoon.domains.realm.behavior import CharacterBehavior
from yakoon.domains.realm.commands.base import RealmCommand
from yakoon.domains.realm.runtime.data import RuntimeRealmData
from yakoon.domains.gateway.runtime.session import GatewaySession
from yakoon.commands.parser import Request


class CmdIC(RealmCommand):

    key = "ic"
    template_key = "account/general/cmd_ic"

    async def run(self, session: GatewaySession, request: Request):
        presenter = await self.get_presenter(session)        
        if not request.args:
            return await presenter.fail("no_name_in_args")

        char_name = request.args[0]
        ns = await self.get_namespace(session)
        services = await self.get_domain_services()
        char = await services.chars.get_by_name(ns, char_name)
        if not char:
            return await presenter.fail("not_found", name=char_name)

        runtime_data: RuntimeRealmData = session.data_runtime
        if runtime_data.character and runtime_data.character.id == char.id:
            return await presenter.emit("already", name=char.name)

        session.data_storage.set(self.controller.id, "char_id", char.id)
        sys_services = await self.get_system_services()
        await sys_services.sessions.save(session)

        CharacterBehavior.attach(char)

        await presenter.emit("success", name=char.name)
        await char.move_to(session, char.location)