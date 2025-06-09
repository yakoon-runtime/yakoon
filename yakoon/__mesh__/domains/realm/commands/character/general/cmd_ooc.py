from yakoon.saas.domains.realm.commands.base import RealmCommand
from yakoon.saas.commands.parser import Request
from yakoon.saas.runtime.models.session import BaseSession


class CmdOOC(RealmCommand):
    
    key = "ooc"
    template_key = "character/general/cmd_ooc"
    requires_character = True

    async def run(self, session: BaseSession, request: Request):
        presenter = await self.get_presenter(session)
        sys_services = await self.get_system_services()
       
        char = session.ctx("realm", "char", persist=False)
        if not char:
            return await presenter.fail("already")

        session.rem_ctx("realm", "char_key", persist=False)
        await sys_services.sessions.save(session)

        await presenter.emit("success", name=char.name)
