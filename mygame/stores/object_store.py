from typing import Optional

from mygame.models.object import Object


class ObjectStore:
    _objects: dict[str, Object] = {}

    @classmethod
    def get(cls, obj_id: str) -> Optional[Object]:
        return cls._objects.get(obj_id)

    @classmethod
    def put(cls, obj: Object):
        cls._objects[obj.id] = obj

    @classmethod
    def contents_of(cls, location_id: str) -> list[Object]:
        return [o for o in cls._objects.values() if o.location == location_id]


ObjectStore.put(
    Object(id="zettel", name="Zettel", desc="Ein alter Zettel.", location="umschlag"))
ObjectStore.put(
    Object(id="umschlag", name="Umschlag", desc="Versiegelt.", location="kiste", contains=["zettel"]))
ObjectStore.put(
    Object(id="kiste", name="Holzkiste", desc="Sieht schwer aus.", location="schank", contains=["umschlag"]))
ObjectStore.put(
    Object(id="schrank", name="Schrank", desc="Ein hölzernes Möbelstück.", location="hall", contains=["kiste"]))
