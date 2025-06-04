from yakoon.bootstrap.setup import setup_system
from yakoon.domains.gateway.controller import GatewayController
from yakoon.runtime.models.session import BaseSession


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
        setup_system(self.service_router, "system")

    async def on_initialize(self, session: BaseSession):
        """
        Called after the controller has been fully constructed but before any commands are processed.

        Use this hook to perform asynchronous setup tasks such as loading data, initializing services,
        or validating infrastructure state (e.g., ensuring the admin account exists).

        This method is guaranteed to run once before the first engine tick or command dispatch.
        """
        await session.emit(f"> [A.M.E.E. online] ✅ Command interface ready.")