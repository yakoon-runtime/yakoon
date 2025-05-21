
from yakoon.domains.game.models.season import Season
from yakoon.domains.game.runtime.clock import Clock
from yakoon.domains.game.stores.season_store import SeasonStore


def get_season(clock: Clock) -> Season | None:
    day = clock.get_time()["day"] % 360 # mathematische Spielwelt

    for s in SeasonStore.all():
        if s.start_day <= s.end_day:
            if s.start_day <= day <= s.end_day:
                return s
        else:  # z. B. start=350, end=20 (Wraparound)
            if day >= s.start_day or day <= s.end_day:
                return s
    return None
