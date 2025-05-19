from yakoon.game.stores.day_phase_store import DayPhaseStore
from yakoon.game.runtime.clock import Clock
from yakoon.game.models.day_phase import DayPhase


def get_day_phase(clock: Clock) -> DayPhase | None:
    hour = clock.get_time()["hour"]

    for phase in DayPhaseStore.all():
        if phase.start_hour <= hour < phase.end_hour:
            return phase
    return None
