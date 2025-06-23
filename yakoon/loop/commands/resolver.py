
from yakoon.loop.runtime.commands.command import MeshCommand


class CommandResolver:
    
    def __init__(self, directory):
        self.directory = directory

    def collect_metadata(self):
        """
        Aggregates all command metadata from all registered controllers.
        """
        result = []
        for controller in self.directory.controllers.values():
            for command_sets in controller.commandsets:
                commands = command_sets.commands()
                if not commands:
                    continue
                result.append({
                    "controller_id": controller.id,
                    "commands": self.collect_commands_data(controller, commands)
                })
        return result
    
    def collect_commands_data(self, controller, commands: list[MeshCommand]):
        keys  = []
        result = []
        for command in commands:
            if command.key in keys:
                raise ValueError(f"Duplicate command key: {controller.id}.{command.key}")
            keys.append(command.key)
            result.append({
                "key": command.key,
                "aliases" : command.aliases
            })
        return result