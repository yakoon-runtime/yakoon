
from collections import defaultdict
from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session import BaseSession


class CmdHelpSystem(Command):

    key = "help"
    template_key = "gateway/system/cmd_help"

    async def run(self, session: BaseSession, request: Request):
        presenter = await self.get_presenter(session)
        grouped = get_grouped_commands(self.controller)

        return await session.fail("ERROR")
        
        registry = await self.get_controller_directory() 
        await presenter.emit(
            "show", controllers=registry.get_controllers(), 
            grouped=grouped)
        

class CmdHelpDomain(Command):

    key = "help"
    template_key = "gateway/system/cmd_help_domain"

    async def run(self, session: BaseSession, request: Request):

        if not request.args:
            grouped = get_grouped_commands(self.controller)
            presenter = await self.get_presenter(session)
            return await presenter.emit("show", controller=self.controller, grouped=grouped)

        # TODO: Hilfe für unsere Commands
        key = request.args[0]
        cmd = self.controller.router.find_by_key_or_alias(key, session.cmd_groups)
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