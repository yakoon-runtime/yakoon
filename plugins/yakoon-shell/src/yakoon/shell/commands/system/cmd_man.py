from pathlib import Path

from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.models.command import CommandScope
from yakoon.base.ports import (
    CommandCatalogService,
    ControllerCatalogService,
    PresenterService,
)
from yakoon.base.runtime.session import Session


class CmdMan(Command):

    key = "man"
    scope = CommandScope.GLOBAL

    template_prefix = "system"

    async def run(self, session: Session, request: Request) -> None:  # noqa: ARG002

        args = request.arg(0)
        if not args:
            await self.show_index(session, request)
        else:
            await self.show_manual(session, request)

    async def show_manual(self, session: Session, request: Request) -> None:
        controller_service = self.services.get(ControllerCatalogService)
        command_service = self.services.get(CommandCatalogService)

        command_key = request.arg(0)
        if not command_key:
            presenter = await self.get_presenter(session)
            await presenter.views.emit("no_manual_entry", command_key="")
            return

        active_controller_id = session.get_active_controller()
        if not active_controller_id:
            active_controller_id = controller_service.shell()[0].id

        # active controller must be listed to show man pages
        if not controller_service.is_listed(active_controller_id):
            return

        # ----------------------------------------------------
        # 1) Try active controller first
        # ----------------------------------------------------
        command = None
        owner_controller_id = active_controller_id

        for c in command_service.for_controller(active_controller_id):
            if c.key == command_key:
                command = c
                break

        # ----------------------------------------------------
        # 2) If not found: try GLOBAL commands from all controllers
        # ----------------------------------------------------
        if not command:
            global_hits: list[tuple[str, object]] = []

            for ctrl in controller_service.all():
                if not controller_service.is_listed(ctrl.id):
                    continue
                for c in command_service.for_controller(ctrl.id):
                    if c.key == command_key and c.scope == CommandScope.GLOBAL:
                        global_hits.append((ctrl.id, c))

            if len(global_hits) == 1:
                owner_controller_id, command = global_hits[0]
            elif len(global_hits) > 1:
                raise RuntimeError(
                    f"Duplicate GLOBAL command key detected: {command_key}"
                )

        # ----------------------------------------------------
        # 3) Render or show "no entry"
        # ----------------------------------------------------
        if not command:
            presenter = await self.get_presenter(session)
            await presenter.views.emit("no_manual_entry", command_key=command_key)
            return

        # controller has to exist - command was found before.
        controller = controller_service.get(owner_controller_id)
        if not controller:
            raise RuntimeError("Controller not found")

        template_source = controller.template_source
        if not template_source:
            raise RuntimeError("Controller has no Templatesource")
        if not template_source.package:
            raise RuntimeError("Templatesource has no package")

        man_folder = template_source.man_folder
        template_key = str(
            Path(template_source.template_sub_path).joinpath(
                man_folder, command.template_prefix, command.key
            )
        )

        presenter_service = self.services.get(PresenterService)
        presenter = await presenter_service.create_presenter(
            template_source.package, template_key, session
        )
        await presenter.views.emit("man_page")

    async def show_index(self, session: Session, request: Request) -> None:

        presenter = await self.get_presenter(session)
        controller_service = self.services.get(ControllerCatalogService)
        command_service = self.services.get(CommandCatalogService)

        shell = controller_service.shell()[0]
        active_controller_id = session.get_active_controller()
        mode = self.resolve_man_mode(request)

        # ----------------------------
        # Shell mode (no active or shell)
        # ----------------------------
        if not active_controller_id or active_controller_id == shell.id:
            # 1) shell commands (defined in shell controller)
            shell_commands = list(
                command_service.for_man_entries(shell.id, session, mode=mode)
            )

            # 2) global commands (defined anywhere)
            globals_by_key: dict[str, object] = {}
            for ctrl in controller_service.all():
                if not controller_service.is_listed(ctrl.id):
                    continue
                for cmd in command_service.for_man_entries(ctrl.id, session, mode=mode):
                    if cmd.scope == CommandScope.GLOBAL:
                        globals_by_key[cmd.key] = cmd

            # merge, avoid duplicates
            merged_by_key: dict[str, object] = {c.key: c for c in shell_commands}
            for k, v in globals_by_key.items():
                merged_by_key.setdefault(k, v)

            shell_commands = sorted(merged_by_key.values(), key=lambda c: c.key)

            controllers = sorted(
                [c for c in controller_service.listed() if c != shell],
                key=lambda c: c.id,
            )

            await presenter.views.emit(
                "show_help",
                mode="shell",
                shell_commands=shell_commands,
                controllers=controllers,
            )
            return

        # ----------------------------
        # Program mode (active != shell)
        # ----------------------------

        # 1) Collect GLOBAL commands from all controllers (system-wide available)
        globals_by_key: dict[str, object] = {}
        for ctrl in controller_service.all():
            # Only include controllers that are listed/visible in this context
            if not controller_service.is_listed(ctrl.id):
                continue

            for cmd in command_service.for_man_entries(ctrl.id, session, mode=mode):
                if cmd.scope == CommandScope.GLOBAL:
                    globals_by_key[cmd.key] = cmd

        # 2) Collect commands from active controller that are executable in program mode
        program_by_key: dict[str, object] = {}
        for cmd in command_service.for_man_entries(
            active_controller_id, session, mode=mode
        ):
            if cmd.scope in (CommandScope.CONTROLLER, CommandScope.GLOBAL):
                program_by_key[cmd.key] = cmd

        # 3) Merge (active controller wins on duplicates, but GLOBAL keys should be unique anyway)
        merged: dict[str, object] = {}
        merged.update(globals_by_key)
        merged.update(program_by_key)

        commands = sorted(merged.values(), key=lambda c: c.key)
        await presenter.views.emit("show_help", mode="program", commands=commands)

    def resolve_man_mode(self, request: Request) -> str:
        if request.has_option("internal"):
            return "internal"
        if request.has_option("all"):
            return "all"
        return "default"
