from yakoon.engine.core.command import Command
from yakoon.engine.core.dialog import ask
from yakoon.engine.core.parser import Request
from yakoon.engine.core.registry import DomainRegistry
from yakoon.platform.render.resolver import render_template_for
from yakoon.platform.runtime.session import PlatformSession
from yakoon.platform.settings import Settings


class CmdSwitch(Command):

    key = "switch"

    async def run(self, session: PlatformSession, request: Request):
        
        name = request.get_arg(0)
        if not name:
            name = await ask(session, "Welche Domain?")
        
        name = name.lower()
        registry: DomainRegistry = getattr(session.ctx, "_registry")
        controller = registry.get_controller_by_name(name)
        if not controller:
            return await session.fail(f"Unbekannte Domain: {name}")

        # sets the current controller.
        session.domain = controller
        session.data_storage.set(
            registry.system.name, "domain", name)

        output = render_template_for(
            Settings.cmd_platform_templates + "system/cmd_switch",
            {"name": controller.name}
        )
        await session.notify(output)
