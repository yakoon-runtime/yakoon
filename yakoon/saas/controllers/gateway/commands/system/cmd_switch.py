from yakoon.mesh.commands.parser import Request
from yakoon.saas.controllers.gateway.commands.base import PlatformCommand
from yakoon.mesh.runtime.session import BaseSession


class CmdSwitch(PlatformCommand):
    
    key = "switch"
    template_key = "system/cmd_switch"

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
