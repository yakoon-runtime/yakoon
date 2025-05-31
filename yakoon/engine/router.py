from __future__ import annotations
from yakoon.core.command import Command

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from yakoon.core.commandset import CommandSet


class CommandRouter:

    def __init__(self):
        self._groups: dict[str, dict[str, type[Command]]] = {}
        self._aliases: dict[str, str] = {}

    def register(self, category: str, cmdset: type[CommandSet], *, append: bool = False):
        if category in self._groups and not append:
            raise ValueError(f"Command group '{category}' already exists. Use append=True to add more commands.")

        group = self._groups.setdefault(category, {})
        for cmd in cmdset.commands():
            key = cmd.key.lower()
            group[key] = cmd
            for alias in getattr(cmd, "aliases", []):
                self._aliases[alias] = key

    def unregister(self, category: str):
        self._groups.pop(category, None)

    def find_by_key_or_alias(self, name: str, groups: list[str] | None = None) -> Command | None:
        if not groups:
            raise ValueError("No command groups provided. Did you forget to set session.cmd_groups?")

        key = name.lower().strip()
        resolved = self._aliases.get(key, key)

        for group in groups:
            cmd = self._groups.get(group, {}).get(resolved)
            if cmd:
                return cmd

        return None

    def resolve(self, name: str, groups: list[str] | None = None) -> Command | None:
        cmd_cls = self.find_by_key_or_alias(name, groups)
        if not cmd_cls:
            return None
        return cmd_cls() if callable(cmd_cls) else cmd_cls
