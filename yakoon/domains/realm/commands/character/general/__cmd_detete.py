
from yakoon.domains.realm.services.object import ObjectService
from yakoon.commands.command import Command
from yakoon.commands.parser import Request
from yakoon.domains.gateway.runtime.session import PlatformSession
from yakoon.runtime.dialogs.prompts import confirm


class __CmdDelete(Command):

    key = "delete"
    aliases = ["del"]

    async def run(self, session: PlatformSession, request: Request):
        obj_id = request.args[0] if request.args else None
        if not obj_id:
            return await session.fail("Bitte gib eine Objekt-ID an.")

        obj = ObjectService.get_by_id(obj_id)
        if not obj:
            return await session.emit(f"Objekt {obj_id} nicht gefunden.")
        if not obj.has_perm(session, "delete"):
            raise PermissionError("Keine Berechtigung zum Löschen.")

        if await confirm(session, f"Wirklich löschen? (y/n) → {obj_id}"):
            await session.emit(f"Objekt '{obj_id}' gelöscht.")
        else:
            await session.emit("Abgebrochen.")
