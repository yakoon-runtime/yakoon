from yakoon.domains.realm.models import ClimateZone


class InMemoryClimateZoneStore:

    def __init__(self):
        self._zones: dict[str, ClimateZone] = {}
        load_defaults(self)

    def add(self, zone: ClimateZone):
        self._zones[zone.id] = zone

    def get_by_id(self, zone_id: str) -> ClimateZone | None:
        return self._zones.get(zone_id)

    def all(self) -> list[ClimateZone]:
        return list(self._zones.values())


def load_defaults(store: InMemoryClimateZoneStore):
    store.add(
        ClimateZone("desert", "Desert", "hot", "dry", "Arid and sun-blasted"))
    store.add(
        ClimateZone("alpine", "Alpine", "cold", "dry", "Snowy highland region"))
    store.add(
        ClimateZone("tropics", "Tropical Jungle", "hot", "humid", "Dense and lush"))
