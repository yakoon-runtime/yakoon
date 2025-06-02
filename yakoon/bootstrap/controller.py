import os
from yakoon.domains.gateway.controller import GatewayController
from yakoon.domains.gateway.runtime.session import GatewaySession
from yakoon.domains.gateway.services.bindings.memory import bind_memory_services
from yakoon.runtime.system.router import ServiceRouter
from yakoon.bootstrap.setup.admin import ensure_admin_account


class BootstrapController(GatewayController):
    """
    Core entry point for the solution.

    Inherit from this controller to define:
    - default command groups
    - solution-specific commandsets
    - lifecycle hooks like on_before_run_command(), etc.

    This replaces the default GatewayController for all solution-specific routing and setup logic.
    """

    def __init__(self):
        super().__init__()    
        self.service_router = ServiceRouter()
        self.service_router.register_static(self.id, bind_memory_services())

    async def on_initialize(self, session: GatewaySession):
        """
        Called after the controller has been fully constructed but before any commands are processed.

        Use this hook to perform asynchronous setup tasks such as loading data, initializing services,
        or validating infrastructure state (e.g., ensuring the admin account exists).

        This method is guaranteed to run once before the first engine tick or command dispatch.
        """
        services = await self.get_gateway_services()
        await ensure_admin_account(services.accounts)
        await session.emit(f"> [A.M.E.E. online] ✅ Command interface ready.")