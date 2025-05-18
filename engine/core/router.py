
from engine.core.command import Command
from engine.core.commandset import CommandSet

class CommandRouter:

    def __init__(self):
        self._groups: dict[str, dict[str, type[Command]]] = {}
        self._aliases: dict[str, str] = {}

    def register(self, name: str, cmdset: type[CommandSet], *, append: bool = False):
        if name in self._groups and not append:
            raise ValueError(f"Command group '{name}' already exists. Use append=True to add more commands.")

        group = self._groups.setdefault(name, {})
        for cmd in cmdset.commands():
            key = cmd.key.lower()
            group[key] = cmd
            for alias in getattr(cmd, "aliases", []):
                self._aliases[alias] = key

    def unregister(self, name: str):
        self._groups.pop(name, None)

    def resolve(self, name: str, groups: list[str] | None = None) -> Command | None:
        if not groups:
            raise ValueError("No command groups provided. Did you forget to set session.command_groups?")
        unknown = [g for g in groups if g not in self._groups]
        if unknown:
            raise ValueError(f"Unknown command groups: {', '.join(unknown)}. Check session.command_groups.")
        key = name.lower().strip()
        resolved = self._aliases.get(key, key)
        active = groups or self._groups.keys()
        for group in active:
            cmd_cls = self._groups.get(group, {}).get(resolved)
            if cmd_cls:
                return cmd_cls()
        return None
