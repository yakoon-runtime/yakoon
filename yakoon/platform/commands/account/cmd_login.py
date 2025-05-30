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

        if not await SessionService.get_by_id(session.id):
            raise ValueError("Session cannot be None")

        session.account_id = account.id
        await SessionService.save(session)

        for controller in session.ctx._registry.get_controllers():
            if hasattr(controller, "on_account_login"):
                await controller.on_account_login(session, account)

        await presenter.emit("login_success", account=account)