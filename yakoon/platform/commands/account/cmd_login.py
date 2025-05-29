from yakoon.engine.core.parser import Request
from yakoon.platform.commands.base import PlatformCommand
from yakoon.platform.render.context import Presenter 
from yakoon.platform.stores.account_store import AccountStore
from yakoon.solution.platform.runtime.session import SolutionSession


class CmdLogin(PlatformCommand):

    key = "login"
    template_key = "account/cmd_login"

    async def run(self, session: SolutionSession, request: Request):

        presenter = self.get_presenter(session)

        if not request.args:
            return await presenter.emit("missing_arg")

        name = request.args[0]
        account = AccountStore.get_by_name(name)
        if not account:
            return await presenter.emit("not_found", name=name)

        session_service = session.ctx.sessions
        pers_session, created = await session_service.get_or_create(
            session.id, account_id=account.id)
        if not pers_session:
            raise ValueError("Session cannot be None")

        await session.ctx.platform.on_account_login(session, account)

        key = "login_success" if created else "returning"
        await presenter.emit(key, account=account)