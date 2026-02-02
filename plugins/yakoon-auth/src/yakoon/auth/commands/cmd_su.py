import asyncio
from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.ports import AuthenticationService, NamespaceService, SessionService
from yakoon.base.runtime.session import Session


class CmdSu(Command):

    key = "su"    

    requires = ["system"]

    async def run(self, session: Session, request: Request):

        presenter = await self.get_presenter(session)
        auth = self.services.get(AuthenticationService)
        namespaces = self.services.get(NamespaceService)
        
        ns = await namespaces.from_session(session)
        
        username = request.get_arg(0) or \
            await presenter.prompts.ask("ask_user")
        secret = request.get_arg(1) or \
            await presenter.prompts.ask_secret("ask_secret") 
        
        result = await auth.authenticate(ns, username, secret)
        if result.ok:
            account = result.account
            session.set_identity(account.key, account.name)
            await self.services.get(SessionService).save(session)
            await presenter.emit("success", user=username)

        else:
            await presenter.emit("failed", 
                                 user=username, 
                                 reason=result.reason)