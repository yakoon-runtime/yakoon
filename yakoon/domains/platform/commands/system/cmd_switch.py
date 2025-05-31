from yakoon.core.parser import Request
from yakoon.engine.registry import DomainRegistry
from yakoon.domains.platform.commands.base import PlatformCommand
from yakoon.domains.platform.runtime.session import PlatformSession
from yakoon.domains.platform.services.session import SessionService


class CmdSwitch(PlatformCommand):
    
    key = "switch"
    template_key = "system/cmd_switch"

    async def run(self, session: PlatformSession, request: Request):
        presenter = await self.get_presenter(session)

        name = request.get_arg(0)
        if not name:
            name = await presenter.prompts.ask("ask_domain")

        name = name.lower()
        registry: DomainRegistry = getattr(session.ctx, "_registry")
        controller = registry.get_controller_by_id(name)

        if not controller:
            return await presenter.fail("not_found", name=name)
        
        session.domain_id = name
        await SessionService.save(session)
        await controller.on_enter(session)

        await presenter.notify("success", name=controller.id)
