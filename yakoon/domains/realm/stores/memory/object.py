from typing import Optional
from yakoon.domains.realm.models.object import Object


class InMemoryObjectStore:

    def __init__(self):
        self._objects: dict[str, Object] = {}
        load_defaults(self)

    def get_by_id(self, obj_id: str) -> Optional[Object]:
        return self._objects.get(obj_id)

    def add(self, obj: Object):
        obj.validate()
        self._objects[obj.id] = obj

    def contents_of(self, location_id: str) -> list[Object]:
        return [o for o in self._objects.values() if o.location == location_id]


def load_defaults(store: InMemoryObjectStore):
    store.add(
        Object(id="zettel", name="Zettel", desc="Ein alter Zettel.", 
               location="umschlag"))
    store.add(
        Object(id="umschlag", name="Umschlag", desc="Versiegelt.", 
               location="kiste", contains=["zettel"]))
    store.add(
        Object(id="kiste", name="Holzkiste", desc="Sieht schwer aus.", 
               location="schrank", contains=["umschlag"]))
    store.add(
        Object(id="schrank", name="Schrank", desc="Ein hölzernes Möbelstück.", 
               location="hall", contains=["kiste"]))
