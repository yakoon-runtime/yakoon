from yakoon.engine.core.parser import Request
from yakoon.platform.commands.base import PlatformCommand
from yakoon.platform.runtime.session import PlatformSession
from yakoon.platform.services.account import AccountService
from yakoon.platform.services.session import SessionService


class CmdLogin(PlatformCommand):

    key = "login"
    template_key = "account/cmd_login"

    async def run(self, session: PlatformSession, request: Request):

        presenter = self.get_presenter(session)

        if not request.args:
            return await presenter.emit("missing_arg")

        name = request.args[0]
        account = await AccountService.get_by_name(name)
        if not account:
            return await presenter.emit("not_found", name=name)

        pers_session, created = await SessionService.get_or_create(session.id)
        if not pers_session:
            raise ValueError("Session cannot be None")

        pers_session.account_id = account.id
        SessionService.save(pers_session)

        await session.ctx.platform.on_account_login(session, account)

        key = "login_success" if created else "returning"
        await presenter.emit(key, account=account)