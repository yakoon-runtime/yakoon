from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session import BaseSession


class CmdSwitch(Command):
    
    key = "switch"
    template_key = "gateway/system/cmd_switch"

    async def run(self, session: BaseSession, request: Request):
        presenter = await self.get_presenter(session)
        services = await self.get_system_services()
        registry = await self.get_controller_directory()

        name = request.get_arg(0)
        if not name:
            name = await presenter.prompts.ask("ask_domain")

        name = name.lower()
        controller = registry.get_controller_by_id(name)
        if not controller:
            return await presenter.fail("not_found", name=name)
        
        session.set_ctx("gateway", "domain_id", controller.id, persist=True)
        await services.sessions.save(session)
        await controller.on_enter(session)

        await presenter.notify("success", name=controller.id)
