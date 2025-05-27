
from collections import defaultdict
from yakoon.engine.core.command import Command
from yakoon.engine.core.parser import Request
from yakoon.platform.runtime.session import PlatformSession


class CmdHelpSystem(Command):

    key = "help"

    async def run(self, session: PlatformSession, request: Request):

        registry = getattr(session.ctx, "_registry")

        await session.emit("Verfügbare Domains:")
        for controller in registry.controllers:
            await session.emit(f"- {controller.name:10}  →  @switch {controller.name}")

        grouped = get_grouped_commands(session.ctx.controller)

        await session.emit(f"\nGlobale Befehle:")
        for category in sorted(grouped):
            await session.emit(f"Kategorie: {category}")
            for cmd in grouped[category]:
                await session.emit(f"- {cmd.key}")


class CmdHelpDomain(Command):

    key = "help"

    async def run(self, session: PlatformSession, request: Request):

        controller = session.ctx.controller
        if not request.args:
            await session.emit(f"Hilfe für Domain: {controller.name}")
            grouped = get_grouped_commands(controller)
            for category in sorted(grouped):
                await session.emit(f"Kategorie: {category}")
                for cmd in grouped[category]:
                    await session.emit(f"- {cmd.key}")
            return

        key = request.args[0]
        cmd = controller.router.find_by_key_or_alias(key, session.cmd_groups)
        if cmd:
            await session.emit(f"Hilfe zu: {cmd.key}")
            await session.emit(cmd.__doc__ or "Keine Beschreibung verfügbar.")
        else:
            await session.fail(f"Befehl '{key}' nicht gefunden.")
    

def get_grouped_commands(controller) -> dict[str, list[Command]]:
    grouped: dict[str, list[Command]] = defaultdict(list)
    for cmdset in controller.commandsets:
        for cmd in cmdset.commands():
            grouped[cmdset.category].append(cmd)
    return grouped