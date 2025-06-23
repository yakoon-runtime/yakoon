from typing import Any, Callable
from dataclasses import dataclass

@dataclass
class CommandProxy:
    key: str
    description: str = ""
    syntax: str = ""

@dataclass
class ControllerProxy:
    id: str
    commands: dict[str, CommandProxy]  # command_id → spec
    websocket: Any  # WebSocket-Verbindung

@dataclass
class Tenent:

    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.controllers: dict[str, ControllerProxy] = {}

    def get_command_proxy(self, command_key: str) -> CommandProxy | None:
        for controller in self.controllers.values():
            if command_key in controller.commands:
                return controller.commands[command_key]
        return None
