from yakoon.game.models.climate_zone import ClimateZone


class ClimateZoneStore:
    _zones: dict[str, ClimateZone] = {}

    @classmethod
    def add(cls, zone: ClimateZone):
        cls._zones[zone.id] = zone

    @classmethod
    def get(cls, zone_id: str) -> ClimateZone | None:
        return cls._zones.get(zone_id)

    @classmethod
    def all(cls) -> list[ClimateZone]:
        return list(cls._zones.values())


ClimateZoneStore.add(ClimateZone("desert", "Desert", "hot", "dry", "Arid and sun-blasted"))
ClimateZoneStore.add(ClimateZone("alpine", "Alpine", "cold", "dry", "Snowy highland region"))
ClimateZoneStore.add(ClimateZone("tropics", "Tropical Jungle", "hot", "humid", "Dense and lush"))
