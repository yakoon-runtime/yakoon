
from pathlib import Path
from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.ports import CommandCatalogService, ControllerCatalogService, PresenterService
from yakoon.base.runtime.session import Session


class CmdMan(Command):

    key = "man"    
    template_prefix = "system"

    async def run(self, session: Session, request: Request):

        args = request.arg(0)
        if not args:
            await self.show_index(session, request)
        else:
            await self.show_manual(session, request)

    async def show_manual(self, session: Session, request: Request):

        controller_service =self.services.get(ControllerCatalogService)
        command_service = self.services.get(CommandCatalogService)

        command_key = request.arg(0)
        active_controller_id = session.get_active_controller()
        if not active_controller_id:
            active_controller_id = controller_service.shell()[0].id

        if not controller_service.is_listed(active_controller_id):
            return

        command = None
        for c in command_service.for_controller(active_controller_id):
            if c.key == command_key:
                command = c
                break

        if not command:
            presenter = await self.get_presenter(session)
            await presenter.emit(
                "no_manual_entry", command_key=command_key)
        else:
            # controller has to exists - command was found before.
            controller = controller_service.get(active_controller_id)
            template_source = controller.template_source

            man_folder = template_source.man_folder
            template_key = str(Path(template_source.template_sub_path).joinpath(
                man_folder, command.template_prefix, command.key))

            presenter_service = self.services.get(PresenterService) 
            presenter = await presenter_service.create_presenter(
                template_source.package,
                template_key, session)

            await presenter.emit("man_page")

                            
    async def show_index(self, session: Session, request: Request):

        presenter = await self.get_presenter(session)
        controller_service =self.services.get(ControllerCatalogService)
        command_service = self.services.get(CommandCatalogService)

        shell = controller_service.shell()[0]
        active_controller_id = session.get_active_controller()

        if not active_controller_id or active_controller_id == shell.id: # shell mode            

            # 1. shell 
            # show alle shell commands
            shell_commands = command_service.for_controller_visible(shell.id, session)
            if shell_commands:
                shell_commands = sorted(shell_commands, key=lambda c: c.key)

            # 2. program
            # (office.mailing, crm.leads, …)
            controllers = []
            for c in controller_service.listed():
                if c != shell:
                    controllers.append(c)

            controllers = sorted(controllers, key=lambda c: c.id)
            await presenter.emit("show_help", 
                                 mode="shell",
                                 shell_commands=shell_commands,
                                 controllers=controllers)
        else: # program mode

            # 1. shell-Builtins
            # builtins (help, use, exit, …)
            commands = []
            for command in command_service.for_controller_visible(shell.id, session):
                if command.key in command_service.shell_builtins():
                    commands.append(command)

            # 2. controller commands            
            commands.extend(
                command_service.for_controller_visible(active_controller_id, session))

            commands = sorted(commands, key=lambda c: c.key)
            await presenter.emit("show_help", 
                            mode='program',
                            commands=commands)