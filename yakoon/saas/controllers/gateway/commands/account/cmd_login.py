from yakoon.saas.commands.parser import Request
from yakoon.saas.controllers.gateway.commands.base import PlatformCommand
from yakoon.saas.runtime.models.session import BaseSession


class CmdLogin(PlatformCommand):

    key = "login"
    template_key = "account/cmd_login"

    async def run(self, session: BaseSession, request: Request):

        presenter = await self.get_presenter(session)
        services = await self.get_gateway_services()

        if not request.args:
            return await presenter.emit("missing_arg")

        name = request.args[0]
        ns = await self.get_namespace(session)
        account = await services.accounts.get_by_name(ns, name)
        if not account:
            return await presenter.emit("not_found", name=name)

        session.set_ctx("gateway", "account_key", account.key, persist=True)
        sys_services = await self.get_system_services()
        await sys_services.sessions.save(session)

        registry = await self.get_controller_directory()
        for controller in registry.get_controllers():
            if hasattr(controller, "on_account_login"):
                await controller.on_account_login(session, account)

        await presenter.emit("login_success", account=account)