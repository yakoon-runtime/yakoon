from yakoon.domains.realm.controller import RealmController
from yakoon.engines.command.registry import DomainRegistry
from yakoon.bootstrap.controller import BootstrapController


class BootstrapRegistry(DomainRegistry):
    """
    Full domain registry for the solution.

    This replaces the default DomainRegistry and defines:
    - the active system controller (BootstrapController)
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
                RealmController(),
            ],
            gateway=BootstrapController(),
        )