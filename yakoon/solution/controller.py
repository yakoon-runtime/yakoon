import os
from yakoon.domains.platform.controller import PlatformController
from yakoon.domains.platform.runtime.session import PlatformSession
from yakoon.solution.setup.bindings import bind_active_storage
from yakoon.solution.setup.init_platform_data import ensure_admin_account


class SolutionMainController(PlatformController):
    """
    Core entry point for the solution.

    Inherit from this controller to define:
    - default command groups
    - solution-specific commandsets
    - lifecycle hooks like on_before_run_command(), etc.

    This replaces the default PlatformController for all solution-specific routing and setup logic.
    """

    def __init__(self):
        super().__init__()    
        bind_active_storage(os.getenv("PLATFORM_STORAGE", "sqlite")) # sqlite

    async def on_initialize(self, session: PlatformSession):
        """
        Called after the controller has been fully constructed but before any commands are processed.

        Use this hook to perform asynchronous setup tasks such as loading data, initializing services,
        or validating infrastructure state (e.g., ensuring the admin account exists).

        This method is guaranteed to run once before the first engine tick or command dispatch.
        """
        await ensure_admin_account()
        await session.emit(f"> [A.M.E.E. online] ✅ Command interface ready.")