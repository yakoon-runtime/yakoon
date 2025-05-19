from engine.core.command import Command
from engine.core.parser import Request
from mygame.runtime.session import GameSession
from mygame.stores.account_store import AccountStore
from mygame.stores.session_store import SessionStore 

class CmdLogin(Command):

    key = "login"

    async def run(self, session: GameSession, request: Request):
        if not request.args:
            return await session.err("Wen willst du anmelden?")

        name = request.args[0]

        account = AccountStore.get_by_name(name)
        if not account:
            return await session.err(f"Account '{name}' nicht gefunden.")
    
        stored = SessionStore.restore(session.id)
        if stored:
            session.account = account
            session.command_groups = ["account"]
            session.update_data(stored)
            return await session.out("Willkommen zurück.")

        # TODO: Hier könnten wir noch nach den character fragen ask_choice....

        session.account = account
        session.command_groups = ["account"]
        SessionStore.persist(session)
        await session.out(f"Du bist angemeldet als {account.name}.")