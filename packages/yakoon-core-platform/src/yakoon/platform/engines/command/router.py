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

    def find(self, active_router_id: str, cmd_name: str) -> tuple[str, Command] | None:
        
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
            command = router.instantiate(cmd_name)
            if command:
                return router.id, command


class CommandRouter:

    def __init__(
        self,
        id: str,
        is_shell: bool,
        is_listed: bool,
        is_activatable: bool,
        builtins: list[str] | None = None
        ):

        self.id = id
        self.is_shell = is_shell
        self.is_listed = is_listed
        self.is_activatable = is_activatable
        self.builtins = builtins or []

        # group_name -> { command_key -> CommandClass }
        self._groups: dict[str, dict[str, type[Command]]] = {}
        # alias -> canonical command_key
        self._aliases: dict[str, str] = {}

    def register(self, group: str, cmdset: type[CommandSet], *, append: bool = False) -> None:
        if group in self._groups and not append:
            raise ValueError(
                f"Command group '{group}' already exists. Use append=True to extend it."
            )

        bucket = self._groups.setdefault(group, {})
        for cmd in cmdset.commands():
            key = cmd.key.lower()
            bucket[key] = cmd

            for alias in getattr(cmd, "aliases", []):
                self._aliases[alias.lower()] = key

    def find_by_key_or_alias(self, name: str) -> type[Command] | None:
        """
        Resolve a command name or alias to a Command class.

        No permission checks.
        No group filtering.
        """
        if not name:
            return None

        key = name.lower().strip()
        resolved = self._aliases.get(key, key)

        # 1) direct match in any group
        for bucket in self._groups.values():
            cmd_cls = bucket.get(resolved)
            if cmd_cls:
                return cmd_cls

        # 2) wildcard fallback ("*") if present
        for bucket in self._groups.values():
            fallback = bucket.get("*")
            if fallback:
                return fallback

        return None

    def instantiate(self, name: str) -> Command | None:
        cmd_cls = self.find_by_key_or_alias(name)
        if not cmd_cls:
            return None
        return cmd_cls()

    def iter_commands(self):
        """
        For man/help only.
        Yields (group_name, command_key, command_cls)
        """
        for group_name, bucket in self._groups.items():
            for cmd_key, cmd_cls in bucket.items():
                if cmd_key == "*":
                    continue
                yield group_name, cmd_key, cmd_cls
