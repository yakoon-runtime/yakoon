
from yakoon.domains.realm.models.season import Season
from yakoon.domains.realm.runtime.clock import Clock
from yakoon.domains.realm.stores.memory.season import InMemorySeasonStore


class SeasonService:

    store = InMemorySeasonStore()

    @classmethod
    def all(cls) -> list[Season]:
        return cls.store.all()

    @classmethod
    def get_season_by_clock(cls, clock: Clock) -> Season | None:
        day = clock.get_time()["day"] % 360 # mathematische Spielwelt

        for s in cls.store.all():
            if s.start_day <= s.end_day:
                if s.start_day <= day <= s.end_day:
                    return s
            else:  # z. B. start=350, end=20 (Wraparound)
                if day >= s.start_day or day <= s.end_day:
                    return s
        return None
