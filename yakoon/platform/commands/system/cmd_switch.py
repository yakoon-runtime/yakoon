from yakoon.engine.core.parser import Request
from yakoon.engine.core.registry import DomainRegistry
from yakoon.platform.commands.base import PlatformCommand
from yakoon.platform.runtime.session import PlatformSession


class CmdSwitch(PlatformCommand):
    
    key = "switch"
    template_key = "system/cmd_switch"

    async def run(self, session: PlatformSession, request: Request):
        presenter = self.get_presenter(session)

        name = request.get_arg(0)
        if not name:
            name = await presenter.prompts.ask("ask_domain")

        name = name.lower()
        registry: DomainRegistry = getattr(session.ctx, "_registry")
        controller = registry.get_controller_by_name(name)

        if not controller:
            return await presenter.fail("not_found", name=name)

        session.domain = controller
        session.data_storage.set(registry.system.name, "domain", name)

        await presenter.notify("success", name=controller.name)
