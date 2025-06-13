
class CommandResolver:

    def __init__(self, controller_directory):
        """
        Initializes the resolver with a ControllerDirectory.
        The directory itself knows which controllers exist,
        but not how to aggregate their metadata.
        """
        self.directory = controller_directory

    def collect_metadata(self):
        """
        Aggregates all command metadata from all registered controllers.
        Expected return: list of dicts with keys like id, name, description, syntax.
        """
        metadata = []
        for controller in self.directory.controllers.values():
            commands = controller.commandsets
            metadata.extend(commands)
        return metadata
