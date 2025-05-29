from yakoon.engine.core.command import Command
from yakoon.engine.core.parser import Request
from yakoon.engine.core.registry import DomainRegistry
from yakoon.platform.render.context import Presenter
from yakoon.platform.runtime.session import PlatformSession


class CmdSwitch(Command):
    
    key = "switch"

    async def run(self, session: PlatformSession, request: Request):
        presenter = Presenter("commands/system/cmd_switch", session)

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
