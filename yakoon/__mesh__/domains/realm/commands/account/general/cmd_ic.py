from yakoon.saas.domains.realm.behavior import CharacterBehavior
from yakoon.saas.domains.realm.commands.base import RealmCommand
from yakoon.saas.runtime.models.session import BaseSession
from yakoon.saas.commands.parser import Request


class CmdIC(RealmCommand):

    key = "ic"
    template_key = "account/general/cmd_ic"

    async def run(self, session: BaseSession, request: Request):
        presenter = await self.get_presenter(session)        
        if not request.args:
            return await presenter.fail("no_name_in_args")

        char_name = request.args[0]
        ns = await self.get_namespace(session)
        services = await self.get_domain_services()

        char = await services.chars.get_by_name(ns, char_name)
        if not char:
            return await presenter.fail("not_found", name=char_name)

        if session.ctx("realm", "char.key", persist=False) == char.key:
            return await presenter.emit("already", name=char.name)

        session.set_ctx("realm", "char_key", char.key, persist=True)
        sys_services = await self.get_system_services()
        await sys_services.sessions.save(session)

        CharacterBehavior.attach(char)

        await presenter.emit("success", name=char.name)
        await char.move_to(session, char.location)