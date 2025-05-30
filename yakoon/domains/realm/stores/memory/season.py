from yakoon.domains.realm.models.season import Season


class InMemorySeasonStore:

    def __init__(self):
        self._seasons: list[Season] = []
        load_defaults(self)

    def all(self) -> list[Season]:
        return self._seasons

    def add(self, season: Season):
        self._seasons.append(season)

    def clear(self):
        self._seasons.clear()


def load_defaults(store: InMemorySeasonStore):
    store.add(Season("frühling", "Frühling", 0, 89))
    store.add(Season("sommer", "Sommer", 90, 179))
    store.add(Season("herbst", "Herbst", 180, 269))
    store.add(Season("winter", "Winter", 270, 359))
