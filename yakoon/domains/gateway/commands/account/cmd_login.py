from yakoon.commands.parser import Request
from yakoon.domains.gateway.commands.base import PlatformCommand
from yakoon.domains.gateway.runtime.session import GatewaySession


class CmdLogin(PlatformCommand):

    key = "login"
    template_key = "account/cmd_login"

    async def run(self, session: GatewaySession, request: Request):

        presenter = await self.get_presenter(session)
        services = await self.get_gateway_services()

        if not request.args:
            return await presenter.emit("missing_arg")

        name = request.args[0]
        account = await services.accounts.get_by_name(name)
        if not account:
            return await presenter.emit("not_found", name=name)

        sys_services = await self.get_system_services()
        if not await sys_services.sessions.get_by_id(session.id):
            raise ValueError("Session cannot be None")

        session.account_id = account.id
        await sys_services.sessions.save(session)

        registry = await self.get_controller_registry()
        for controller in registry.get_controllers():
            if hasattr(controller, "on_account_login"):
                await controller.on_account_login(session, account)

        await presenter.emit("login_success", account=account)