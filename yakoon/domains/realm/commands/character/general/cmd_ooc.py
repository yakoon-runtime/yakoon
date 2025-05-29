from yakoon.domains.realm.commands.base import RealmCommand
from yakoon.domains.realm.runtime.data import RuntimeRealmData
from yakoon.engine.core.parser import Request
from yakoon.solution.platform.runtime.session import SolutionSession

class CmdOOC(RealmCommand):
    
    key = "ooc"
    template_key = "character/general/cmd_ooc"
    requires_character = True

    async def run(self, session: SolutionSession, request: Request):
        presenter = self.get_presenter(session)
       
        runtime_data: RuntimeRealmData = session.data_runtime
        if not runtime_data.character:
            return await presenter.fail("already")

        name = runtime_data.character.name
        session.data_storage.rem(session.ctx.controller.name, "char_id")

        await presenter.emit("success", name=name)
