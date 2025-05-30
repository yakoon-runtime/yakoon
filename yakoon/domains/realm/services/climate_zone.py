
from yakoon.domains.realm.models.climate_zone import ClimateZone
from yakoon.domains.realm.stores.memory.climate_zone import InMemoryClimateZoneStore


class ClimateZoneService:

    store = InMemoryClimateZoneStore()

    @classmethod
    def get_by_id(cls, zone_id: str) -> ClimateZone | None:
        return cls.store.get_by_id(zone_id)

    @classmethod
    def all(cls) -> list[ClimateZone]:
        return cls.store.all()
