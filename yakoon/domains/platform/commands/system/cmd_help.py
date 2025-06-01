
from collections import defaultdict
from yakoon.core.command import Command
from yakoon.core.parser import Request
from yakoon.domains.platform.commands.base import PlatformCommand
from yakoon.domains.platform.runtime.session import PlatformSession


class CmdHelpSystem(PlatformCommand):

    key = "help"
    template_key = "system/cmd_help"

    async def run(self, session: PlatformSession, request: Request):
        registry = getattr(session.ctx, "_registry")
        grouped = get_grouped_commands(session.ctx.controller)

        presenter = await self.get_presenter(session)
        await presenter.emit(
            "show", controllers=registry.get_controllers(), 
            grouped=grouped)
        

class CmdHelpDomain(PlatformCommand):

    key = "help"
    template_key = "system/cmd_help_domain"

    async def run(self, session: PlatformSession, request: Request):

        controller = session.ctx.controller
        if not request.args:
            grouped = get_grouped_commands(controller)
            presenter = await self.get_presenter(session)
            return await presenter.emit("show", controller=controller, grouped=grouped)

        # TODO: Hilfe für unsere Commands
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