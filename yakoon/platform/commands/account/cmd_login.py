from yakoon.engine.core.command import Command
from yakoon.engine.core.parser import Request
from yakoon.platform.render.resolver import render_template_for
from yakoon.platform.settings import Settings
from yakoon.platform.stores.account_store import AccountStore
from yakoon.solution.platform.runtime.session import SolutionSession


class CmdLogin(Command):

    key = "login"

    async def run(self, session: SolutionSession, request: Request):
        if not request.args:
            return await session.fail("Wen willst du anmelden?")

        name = request.args[0]
        account = AccountStore.get_by_name(name)
        if not account:
            return await session.fail(f"Account '{name}' nicht gefunden.")
        
        session_service = session.ctx.sessions
        pers_session, created = await session_service.get_or_create(session.id, account_id=account.id)
        if not pers_session:
            raise ValueError("Session cannot be None")

        await session.ctx.platform.on_account_login(session, account)
        output = render_template_for(
                Settings.cmd_platform_templates + "account/cmd_login",
                {"account": account, "returning": not created}
            )
        await session.emit(output)
