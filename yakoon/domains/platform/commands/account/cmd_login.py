from yakoon.core.parser import Request
from yakoon.domains.platform.commands.base import PlatformCommand
from yakoon.domains.platform.runtime.session import PlatformSession


class CmdLogin(PlatformCommand):

    key = "login"
    template_key = "account/cmd_login"

    async def run(self, session: PlatformSession, request: Request):

        presenter = await self.get_presenter(session)
        services = await self.get_services(session)

        if not request.args:
            return await presenter.emit("missing_arg")

        name = request.args[0]
        account = await services.accounts.get_by_name(name)
        if not account:
            return await presenter.emit("not_found", name=name)

        if not await services.sessions.get_by_id(session.id):
            raise ValueError("Session cannot be None")

        session.account_id = account.id
        await services.sessions.save(session)

        for controller in session.ctx._registry.get_controllers():
            if hasattr(controller, "on_account_login"):
                await controller.on_account_login(session, account)

        await presenter.emit("login_success", account=account)