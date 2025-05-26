from yakoon.engine.core.command import Command
from yakoon.engine.core.dialog import ask
from yakoon.engine.core.parser import Request
from yakoon.engine.core.registry import DomainRegistry
from yakoon.platform.runtime.session import PlatformSession


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
            return await session.send_error(f"Unbekannte Domain: {name}")

        session.domain = controller
        await session.send_status(f"Du bist jetzt in {controller.name.upper()}.")

        # Domain can decide to login to domain
        await controller.on_enter(session)
