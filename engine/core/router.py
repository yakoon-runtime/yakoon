
from typing import Type
from engine.core.command import Command

class CommandRouter:
    
    def __init__(self):
       self._aliases: dict[str, str] = {}
       self._session_commands = {}
       self._commands_by_mode = {
            "account": {},
            "character": {},
            "system": {},
            "dynamic": {},  # optional: per session.id
        }
            
    def register(self, cmd_cls, mode: str = "system", session=None):
        key = cmd_cls.key.lower()
        group = self._commands_by_mode.setdefault(mode, {})

        if session and mode == "dynamic":
            sid = session.id
            self._session_commands.setdefault(sid, []).append(cmd_cls)
        else:
            group[key] = cmd_cls
            for alias in getattr(cmd_cls, "aliases", []):
                self._aliases[alias] = key

    def register_dynamic_commands(self, cmd, session):
        self.register(cmd, "dynamic", session=session)         

    def remove_dynamic_commands_for_session(self, session):
        self._session_commands[session.id] = []

    def resolve(self, cmd_name: str, session=None) -> Command | None:
        key = cmd_name.lower().strip()
        resolved = self._aliases.get(key, key)

        modes = ["system"]

        if session:
            modes.append("character" if session.character else "account")
            for cmd_cls in self._session_commands.get(session.id, []):
                if resolved == cmd_cls.key or resolved in getattr(cmd_cls, "aliases", []):
                    return cmd_cls

        for mode in modes:
            group = self._commands_by_mode.get(mode, {})
            if resolved in group:
                return group[resolved]()

        return None
