from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yakoon.base.commands.command import Command
    from yakoon.base.commands.commandset import CommandSet


class CommandDirectory:

    def __init__(self):
        self._routers: list[CommandRouter] = []        

    def register(self, router_name, router: CommandRouter):
        router.id = router_name
        self._routers.append(router)

    def find(self, active_router_id: str, cmd_name: str, cmd_groups: list[str] | None = None) -> tuple[str, Command] | None:
        
        eligible_routers = None

        if active_router_id is None: 
            # Shell mode
            
            eligible_routers = [r for r in self._routers]
        else:                       
            # Fokusmodus
            
            eligible_routers = [
                r for r in self._routers 
                if r.is_shell or (r.is_activatable and r.id == active_router_id)]

        for router in eligible_routers:
            command = router.instantiate(cmd_name, cmd_groups)
            if command:
                return router.id, command


class CommandRouter:

    def __init__(self, is_shell, is_listed, is_activatable):
        
        self.is_shell = is_shell
        self.is_listed = is_listed
        self.is_activatable = is_activatable

        self._groups: dict[str, dict[str, type[Command]]] = {}
        self._aliases: dict[str, str] = {}

    def register(self, category: str, cmdset: type[CommandSet], *, append: bool = False):
        if category in self._groups and not append:
            raise ValueError(f"MeshCommand group '{category}' already exists. Use append=True to add more commands.")

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
            
        # fallback: check for key = "*"
        for group in groups:
            fallback = self._groups.get(group, {}).get("*")
            if fallback:
                return fallback

        return None

    def instantiate(self, name: str, groups: list[str] | None = None) -> Command | None:
        cmd_cls = self.find_by_key_or_alias(name, groups)
        if not cmd_cls:
            return None
        return cmd_cls() if callable(cmd_cls) else cmd_cls
