from yakoon.platform.controller import PlatformController


class SolutionMainController(PlatformController):
    """
    Core entry point for the solution.

    Inherit from this controller to define:
    - default command groups
    - solution-specific commandsets
    - lifecycle hooks like on_before_send(), on_before_run_command(), etc.

    This replaces the default PlatformController for all solution-specific routing and setup logic.
    """

    # Example: override default_command_groups = ["your:group"]
    # def commandsets = [MyCommandSet]
    # def on_before_send(self, session, msg): ...
    pass