
from dataclasses import asdict
from typing import Iterable, Sequence

from yakoon.base.models.catalog import CommandInfo, ControllerInfo


class CommandCatalog:

    def __init__(self, commands: Iterable[CommandInfo], shell_builtins: Sequence[str] = ()):
        self._commmands = commands
        self._shell_builtins = set(shell_builtins)

    def all(self):
        return self._commmands
    
    def builtins(self):
        return self._shell_builtins


class CommandCatalogService:

    __slots__ = ("_by_controller", "_shell_builtins")

    def __init__(self, catalog: CommandCatalog):
        by_controller: dict[str, list[CommandInfo]] = {}
        for c in catalog.all():
            by_controller.setdefault(c.controller_id, []).append(c)

        # stabile Ordnung
        for _, items in by_controller.items():
            items.sort(key=lambda x: x.key)

        self._by_controller = by_controller
        self._shell_builtins = set(catalog.builtins())

    def for_controller(self, controller_id: str) -> Sequence[CommandInfo]:
        return tuple(self._by_controller.get(controller_id, ()))

    def keys_for_controller(self, controller_id: str) -> Sequence[str]:
        return tuple(c.key for c in self.for_controller(controller_id))

    def is_shell_builtin(self, key: str) -> bool:
        return key in self._shell_builtins

    def shell_builtins(self) -> Sequence[str]:
        return tuple(sorted(self._shell_builtins))


class ControllerCatalog:
    
    def __init__(self, controllers: Iterable[ControllerInfo]):
        self._controllers = controllers

    def all(self):
        return self._controllers


class ControllerCatalogService:
    """
    Read-only snapshot about controller metadata.
    No controller instance, no directory references.
    """

    __slots__ = ("_by_id",)

    def __init__(self, catalog: ControllerCatalog):
        by_id: dict[str, ControllerInfo] = {}
        for c in catalog.all():
            if c.id in by_id:
                raise ValueError(f"Duplicate controller id in catalog: {c.id}")
            by_id[c.id] = c
        self._by_id = by_id

    def ids(self) -> Sequence[str]:
        return tuple(sorted(self._by_id.keys()))

    def all(self) -> Sequence[ControllerInfo]:
        return tuple(self._by_id[cid] for cid in self.ids())

    def get(self, controller_id: str) -> ControllerInfo | None:
        return self._by_id.get(controller_id)

    def exists(self, controller_id: str) -> bool:
        return controller_id in self._by_id

    def activatable(self) -> Sequence[ControllerInfo]:
        return tuple(c for c in self.all() if c.is_activatable)

    def listed(self) -> Sequence[ControllerInfo]:
        return tuple(c for c in self.all() if c.is_listed)

    def shell(self) -> Sequence[ControllerInfo]:
        return tuple(c for c in self.all() if c.is_shell)

    def is_shell(self, controller_id: str) -> bool:
        c = self.get(controller_id)
        return bool(c and c.is_shell)

    def is_activatable(self, controller_id: str) -> bool:
        c = self.get(controller_id)
        return bool(c and c.is_activatable)

    def is_listed(self, controller_id: str) -> bool:
        c = self.get(controller_id)
        return bool(c and c.is_listed)
        