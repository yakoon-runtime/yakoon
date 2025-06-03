from yakoon.commands.parser import Request
from yakoon.engines.command.registry import DomainRegistry
from yakoon.domains.gateway.commands.base import PlatformCommand
from yakoon.domains.gateway.runtime.session import GatewaySession


class CmdSwitch(PlatformCommand):
    
    key = "switch"
    template_key = "system/cmd_switch"

    async def run(self, session: GatewaySession, request: Request):
        presenter = await self.get_presenter(session)
        services = await self.get_system_services()
        registry = await self.get_controller_registry()

        name = request.get_arg(0)
        if not name:
            name = await presenter.prompts.ask("ask_domain")

        name = name.lower()
        controller = registry.get_controller_by_id(name)
        if not controller:
            return await presenter.fail("not_found", name=name)
        
        session.domain_id = name
        await services.sessions.save(session)
        await controller.on_enter(session)

        await presenter.notify("success", name=controller.id)
