from yakoon.domains.realm.commands.base import RealmCommand
from yakoon.domains.realm.runtime.data import RuntimeRealmData
from yakoon.commands.parser import Request
from yakoon.domains.gateway.runtime.session import GatewaySession


class CmdOOC(RealmCommand):
    
    key = "ooc"
    template_key = "character/general/cmd_ooc"
    requires_character = True

    async def run(self, session: GatewaySession, request: Request):
        presenter = await self.get_presenter(session)
       
        runtime_data: RuntimeRealmData = session.data_runtime
        if not runtime_data.character:
            return await presenter.fail("already")

        name = runtime_data.character.name
        session.data_storage.rem(self.controller.id, "char_id")

        await presenter.emit("success", name=name)
