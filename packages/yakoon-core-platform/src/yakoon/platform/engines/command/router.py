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
        
        eligible_routers = []
        shell = [r for r in self._routers if r.is_shell and r.is_activatable][0]

        if shell.id == active_router_id:
            # only shell router is active
            eligible_routers = [shell]
        else:                       
            # router from active controller and shell builtins 
            eligible_routers = [
                r for r in self._routers \
                    if r.id == active_router_id and r.is_activatable or r.is_shell]

        for router in eligible_routers:
            if active_router_id != shell.id and router.id == shell.id:
                if cmd_name not in shell.builtins:
                    continue
            command = router.instantiate(cmd_name, cmd_groups)
            if command:
                return router.id, command


class CommandRouter:

    id: str = None

    def __init__(self, id, is_shell, is_listed, is_activatable, builtins=[]):       
        self.id = id
        self.is_shell = is_shell
        self.is_listed = is_listed
        self.is_activatable = is_activatable
        self.builtins = builtins

        self._groups: dict[str, dict[str, type[Command]]] = {}
        self._aliases: dict[str, str] = {}

    def register(self, group: str, cmdset: type[CommandSet], *, append: bool = False):
        if group in self._groups and not append:
            raise ValueError(f"Command group '{group}' already exists. Use append=True to add more commands.")

        group = self._groups.setdefault(group, {})
        for cmd in cmdset.commands():
            key = cmd.key.lower()
            group[key] = cmd
            for alias in getattr(cmd, "aliases", []):
                self._aliases[alias] = key

    def unregister(self, group: str):
        self._groups.pop(group, None)

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
