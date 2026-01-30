from yakoon.base.ports import SessionService
from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session import Session


class CmdLogin(Command):

    key = "login"
    template_key = "gateway/account/cmd_login"

    async def run(self, session: Session, request: Request):

        presenter = await self.get_presenter(session)

        if not request.args:
            return await presenter.emit("missing_arg")

        name = request.args[0]
        ns = await self.get_namespace(session)
        accounts = self.services.get(AccountService)
        account = await accounts.get_by_name(ns, name)
        if not account:
            return await presenter.emit("not_found", name=name)

        session.set_ctx("gateway", "account_key", account.key, persist=True)
        sessions = self.services.get(SessionService)
        await sessions.save(session)

        await presenter.emit("login_success", account=account)