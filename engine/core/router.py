
from typing import Type
from engine.core.command import Command

class CommandRouter:
    
    def __init__(self, engine):
        self._commands: dict[str, Type[Command]] = {}
        self._session_commands = {}
        self._aliases: dict[str, str] = {}
        self._engine = engine

    def register(self, command_cls: Type[Command], dynamic=False, session=None):
        command_cls._engine = self._engine
        if dynamic and session:
            self._session_commands.setdefault(session.id, []).append(command_cls)
        else:
            self._commands[command_cls.key] = command_cls
            for alias in getattr(command_cls, "aliases", []):
                self._aliases[alias] = command_cls.key

    def remove_dynamic_commands_for_session(self, session):
        self._session_commands[session.id] = []

    def resolve(self, cmd_name: str, session=None) -> Command | None:
        key = cmd_name.lower().strip()
        resolved = self._aliases.get(key, key)
        # 1. try: globale Commands
        if resolved in self._commands:
            return self._commands[resolved]()
        # 2. try: dynamic commands for these session
        if session:
            for cmd_cls in self._session_commands.get(session.id, []):
                if resolved == cmd_cls.key or resolved in getattr(cmd_cls, "aliases", []):
                    return cmd_cls  # important: get an instance

        return None
