
from collections import defaultdict
from yakoon.engine.core.command import Command
from yakoon.engine.core.parser import Request
from yakoon.platform.render.resolver import render_template_for
from yakoon.platform.runtime.session import PlatformSession
from yakoon.platform.settings import Settings


class CmdHelpSystem(Command):

    key = "help"

    async def run(self, session: PlatformSession, request: Request):
        registry = getattr(session.ctx, "_registry")
        grouped = get_grouped_commands(session.ctx.controller)
        output = render_template_for(
            Settings.cmd_platform_templates + "system/cmd_help",
            {
                "controllers": [registry.system] + registry.controllers,
                "grouped": grouped,
            }
        )
        await session.emit(output)
        

class CmdHelpDomain(Command):

    key = "help"

    async def run(self, session: PlatformSession, request: Request):

        controller = session.ctx.controller
        if not request.args:
            grouped = get_grouped_commands(controller)
            output = render_template_for(
                Settings.cmd_platform_templates + "system/cmd_help_domain",
                {
                    "controller": controller,
                    "grouped": grouped
                }
            )
            await session.emit(output)
            return

        key = request.args[0]
        cmd = controller.router.find_by_key_or_alias(key, session.cmd_groups)
        if cmd:
            await session.emit(f"Hilfe zu: {cmd.key}")
            await session.emit(cmd.__doc__ or "Keine Beschreibung verfügbar.")
        else:
            await session.send_error(f"Befehl '{key}' nicht gefunden.")
    

def get_grouped_commands(controller) -> dict[str, list[Command]]:
    grouped: dict[str, list[Command]] = defaultdict(list)
    for cmdset in controller.commandsets:
        for cmd in cmdset.commands():
            grouped[cmdset.category].append(cmd)
    return grouped