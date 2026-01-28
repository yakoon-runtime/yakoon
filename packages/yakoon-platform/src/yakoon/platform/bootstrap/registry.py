from yakoon.platform.controllers.directory import ControllerDirectory
from yakoon.platform.controllers.mesh.controller import MeshController
from yakoon.platform.bootstrap.controller import BootstrapController


class BootstrapControllerDirectory(ControllerDirectory):
    """
    Full domain registry for the solution.

    This replaces the default ControllerDirectory and defines:
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
                MeshController()
            ],
            gateway=BootstrapController(),
        )

