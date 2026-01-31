
from typing import Iterable, Sequence

from yakoon.base.models.catalog import ControllerInfo


class ControllerCatalog:
    """
    Read-only snapshot about controller metadata.
    No controller instance, no directory references.
    """

    __slots__ = ("_by_id",)

    def __init__(self, controllers: Iterable[ControllerInfo]):
        by_id: dict[str, ControllerInfo] = {}
        for c in controllers:
            if c.id in by_id:
                raise ValueError(f"Duplicate controller id in catalog: {c.id}")
            by_id[c.id] = c
        self._by_id = by_id

    def ids(self) -> Sequence[str]:
        return tuple(sorted(self._by_id.keys()))

    def get_all(self) -> Sequence[ControllerInfo]:
        return tuple(self._by_id[cid] for cid in self.ids())

    def get(self, controller_id: str) -> ControllerInfo | None:
        return self._by_id.get(controller_id)

    def exists(self, controller_id: str) -> bool:
        return controller_id in self._by_id

    def activatable(self) -> Sequence[ControllerInfo]:
        return tuple(c for c in self.all() if c.is_activatable)

    def global_visible(self) -> Sequence[ControllerInfo]:
        return tuple(c for c in self.all() if c.is_global_visible)

    def shell(self) -> Sequence[ControllerInfo]:
        return tuple(c for c in self.all() if c.is_shell)

    def global_visible(self) -> Sequence[ControllerInfo]:
        return tuple(c for c in self.all() if c.is_global_visible)

    def is_shell(self, controller_id: str) -> bool:
        c = self.get(controller_id)
        return bool(c and c.is_shell)

    def is_activatable(self, controller_id: str) -> bool:
        c = self.get(controller_id)
        return bool(c and c.is_activatable)

    def is_global_visible(self, controller_id: str) -> bool:
        c = self.get(controller_id)
        return bool(c and c.is_global_visible)


class SystemCatalogService:
    
    _controllers: ControllerCatalog

    def __init__(self, controllers: ControllerCatalog):
       self._controllers = controllers

    def get_controller_catalog(self) -> ControllerCatalog:
       return self._controllers
        
    