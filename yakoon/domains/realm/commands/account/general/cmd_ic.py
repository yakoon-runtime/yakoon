from yakoon.domains.realm.behavior import CharacterBehavior
from yakoon.domains.realm.commands.base import RealmCommand
from yakoon.domains.realm.runtime.data import RuntimeRealmData
from yakoon.domains.realm.stores.character_store import CharacterStore
from yakoon.engine.core.parser import Request
from yakoon.solution.platform.runtime.session import SolutionSession


class CmdIC(RealmCommand):

    key = "ic"
    template_key = "account/general/cmd_ic"

    async def run(self, session: SolutionSession, request: Request):
        presenter = self.get_presenter(session)

        if not request.args:
            return await presenter.fail("no_name_in_args")

        char_name = request.args[0]
        char = CharacterStore.get_by_name(char_name)

        if not char:
            return await presenter.fail("not_found", name=char_name)

        runtime_data: RuntimeRealmData = session.data_runtime
        if runtime_data.character and runtime_data.character.id == char.id:
            return await presenter.emit("already", name=char.name)

        session.data_storage.set(session.ctx.controller.name, "char_id", char.id)
        await session.ctx.sessions.persist(session)

        CharacterBehavior.attach(char)

        await presenter.emit("success", name=char.name)
        await char.move_to(session, char.location)