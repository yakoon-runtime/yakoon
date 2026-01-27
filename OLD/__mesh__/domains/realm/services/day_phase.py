
from yakoon.platform.domains.realm.runtime.clock import Clock
from yakoon.platform.domains.realm.models.day_phase import DayPhase
from yakoon.platform.domains.realm.stores.memory.day_phase import InMemoryDayPhaseStore


class DayPhaseService:

    store = InMemoryDayPhaseStore()

    @classmethod
    def all(cls) -> list[DayPhase]:
        return cls.store.all()
 
    @classmethod
    def get_day_phase_by_clock(cls, clock: Clock) -> DayPhase | None:
        hour = clock.get_time()["hour"]

        for phase in cls.store.all():
            if phase.start_hour <= hour < phase.end_hour:
                return phase
        return None
