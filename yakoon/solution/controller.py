from yakoon.platform.controller import PlatformController
from yakoon.solution.platform.runtime.session import SolutionSession


class SolutionMainController(PlatformController):
    """
    Core entry point for the solution.

    Inherit from this controller to define:
    - default command groups
    - solution-specific commandsets
    - lifecycle hooks like on_before_send(), on_before_run_command(), etc.

    This replaces the default PlatformController for all solution-specific routing and setup logic.
    """

    async def on_ready(self, session: SolutionSession):
        await session.emit(f"> [A.M.E.E. online] ✅ Command interface ready.")