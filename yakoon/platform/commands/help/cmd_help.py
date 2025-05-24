
from collections import defaultdict
from yakoon.engine.core.command import Command
from yakoon.engine.core.parser import Request
from yakoon.platform.commands.command import PlatformCommand
from yakoon.platform.runtime.session import PlatformSession


class CmdHelpSystem(PlatformCommand):

    key = "help"

    async def run(self, session: PlatformSession, request: Request):

        registry = getattr(session.ctx, "_registry")

        await session.send_msg("Verfügbare Domains:")
        for controller in registry.controllers:
            await session.send_msg(f"- {controller.name:10}  →  @switch {controller.name}")

        grouped = _get_grouped_commands(session.ctx.controller)

        await session.send_msg(f"\nGlobale Befehle:")
        for category in sorted(grouped):
            await session.send_msg(f"Kategorie: {category}")
            for cmd in grouped[category]:
                await session.send_msg(f"- {cmd.key}")


class CmdHelpDomain(PlatformCommand):

    key = "help"

    async def run(self, session: PlatformSession, request: Request):

        controller = session.ctx.controller
        if not request.args:
            await session.send_msg(f"Hilfe für Domain: {controller.name}")
            grouped = _get_grouped_commands(controller)
            for category in sorted(grouped):
                await session.send_msg(f"Kategorie: {category}")
                for cmd in grouped[category]:
                    await session.send_msg(f"- {cmd.key}")
            return

        key = request.args[0]
        cmd = controller.router.find_by_key(key, session.command_groups)
        if cmd:
            await session.send_msg(f"Hilfe zu: {cmd.key}")
            await session.send_msg(cmd.__doc__ or "Keine Beschreibung verfügbar.")
        else:
            await session.send_error(f"Befehl '{key}' nicht gefunden.")
    

def _get_grouped_commands(controller) -> dict[str, list[Command]]:
    grouped: dict[str, list[Command]] = defaultdict(list)
    for cmdset in controller.commandsets:
        for cmd in cmdset.commands():
            grouped[cmdset.category].append(cmd)
    return grouped
