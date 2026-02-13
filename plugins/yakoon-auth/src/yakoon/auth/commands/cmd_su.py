import asyncio
from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.ports import (
    AuthenticationService,
    NamespaceService,
    PermissionService,
    SessionService,
)
from yakoon.base.runtime.session import Session


class CmdSu(Command):

    key = "su"

    async def run(self, session: Session, request: Request):

        presenter = await self.get_presenter(session)
        auth = self.services.get(AuthenticationService)
        namespaces = self.services.get(NamespaceService)
        permissions = self.services.get(PermissionService)

        ns = await namespaces.from_session(session)

        username = (
            request.arg(0)
            or request.option("user")
            or await presenter.prompts.ask("ask_user")
        )
        secret = request.option("password") or await presenter.prompts.ask_secret(
            "ask_secret"
        )

        result = await auth.authenticate(ns, username, secret)
        if result.ok:
            account = result.account
            session.set_identity(account.key, account.username)
            permissions.apply_account_permissions(session, account)

            await self.services.get(SessionService).save(session)
            await presenter.emit("success", user=username)

        else:
            await presenter.emit("failed", user=username, reason=result.reason)
