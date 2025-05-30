from yakoon.engine.core.registry import DomainRegistry
from yakoon.platform.services.session import SessionService
from yakoon.solution.controller import SolutionMainController
from yakoon.solution.domains.realm.controller import SolutionRealmController


class SolutionRegistry(DomainRegistry):
    """
    Full domain registry for the solution.

    This replaces the default DomainRegistry and defines:
    - the active system controller (SolutionController)
    - the list of registered domain controllers (e.g. Mud, Office, Industry, etc)
    - the session service and store used to manage user sessions

    All application entrypoints (console, webapi, telnet, etc.)
    should import and use this registry to ensure consistent configuration.

    Override or extend this class if you want to dynamically inject
    domains, session logic, or customize system behavior per deployment.
    """
  
    def __init__(self):        
        super().__init__(
            controllers=[
                SolutionRealmController(),
            ],
            system=SolutionMainController(),
            sessions=SessionService,
        )