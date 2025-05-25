
from yakoon.engine.core.command import Command
from yakoon.engine.core.dialog import confirm
from yakoon.engine.core.parser import Request
from yakoon.domains.game.stores.object_store import ObjectStore
from yakoon.solution.platform.runtime.session import SolutionSession


class CmdDelete(Command):
    key = "delete"
    aliases = ["del"]

    async def run(self, session: SolutionSession, request: Request):
        obj_id = request.args[0] if request.args else None
        if not obj_id:
            return await session.err("Bitte gib eine Objekt-ID an.")

        obj = ObjectStore.get(obj_id)
        if not obj:
            return await session.out(f"Objekt {obj_id} nicht gefunden.")
        if not obj.has_perm(session, "delete"):
            raise PermissionError("Keine Berechtigung zum Löschen.")

        if await confirm(session, f"Wirklich löschen? (y/n) → {obj_id}"):
            await session.out(f"Objekt '{obj_id}' gelöscht.")
        else:
            await session.out("Abgebrochen.")
