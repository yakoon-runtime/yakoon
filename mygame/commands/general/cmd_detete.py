
from engine.core.command import Command
from engine.core.dialog import confirm
from engine.core.parser import Request
from engine.runtime.session import Session


class CmdDelete(Command):
    key = "delete"
    aliases = ["del"]

    async def run(self, session: Session, request: Request):
        target_id = request.args[0] if request.args else None
        if not target_id:
            return await session.err("Bitte gib eine Objekt-ID an.")

        if await confirm(session, f"Wirklich löschen? (y/n) → {target_id}"):
            await session.out(f"Objekt '{target_id}' gelöscht.")
        else:
            await session.out("Abgebrochen.")

        answer = await confirm(session, f"Neu anlegen? (y/n) → {target_id}")
        if answer:
            await session.out(f"Objekt '{target_id}' angelegt.")
        else:
            await session.out("Abgebrochen.")