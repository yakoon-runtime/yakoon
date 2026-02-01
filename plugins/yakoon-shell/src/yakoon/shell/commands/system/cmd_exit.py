from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.ports import ControllerCatalogService, SessionService
from yakoon.base.runtime.session import Session


class CmdExit(Command):

    key = "exit"    
    template_prefix = "system"

    requires = ["system"]

    async def run(self, session: Session, request: Request):

        controllers = self.services.get(ControllerCatalogService)
        presenter = await self.get_presenter(session)

        shell = controllers.shell()[0]
        active_controller_id = session.get_active_controller()
        if shell.id == active_controller_id:
            await presenter.emit("shell.already_in_shell", controller=shell)
        else:
            session.set_active_controller(shell.id)
            await self.services.get(SessionService).save(session)
            await presenter.emit("shell.exit_app", controller=shell)
