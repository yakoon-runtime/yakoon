from yakoon.domains.realm.models.season import Season


class SeasonStore:
    _seasons: list[Season] = []

    @classmethod
    def all(cls) -> list[Season]:
        return cls._seasons

    @classmethod
    def add(cls, season: Season):
        cls._seasons.append(season)

    @classmethod
    def clear(cls):
        cls._seasons.clear()


SeasonStore.add(Season("frühling", "Frühling", 0, 89))
SeasonStore.add(Season("sommer", "Sommer", 90, 179))
SeasonStore.add(Season("herbst", "Herbst", 180, 269))
SeasonStore.add(Season("winter", "Winter", 270, 359))
