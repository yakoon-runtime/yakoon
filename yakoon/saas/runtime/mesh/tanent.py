from typing import Any, Callable
from dataclasses import dataclass

@dataclass
class CommandProxy:
    id: str
    name: str
    description: str = ""
    syntax: str = ""

@dataclass
class ControllerProxy:
    controller_id: str
    commands: dict[str, CommandProxy]  # command_id → spec
    websocket: Any  # WebSocket-Verbindung

class Tanent:
    def __init__(self, tenant_id: str):
        self.controllers: dict[str, ControllerProxy] = {}
