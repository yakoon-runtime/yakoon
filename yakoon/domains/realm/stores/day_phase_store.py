
from yakoon.domains.realm.models.day_phase import DayPhase


class DayPhaseStore:
    _phases: list[DayPhase] = []

    @classmethod
    def all(cls) -> list[DayPhase]:
        return cls._phases

    @classmethod
    def add(cls, phase: DayPhase):
        cls._phases.append(phase)

    @classmethod
    def clear(cls):
        cls._phases.clear()


DayPhaseStore.add(DayPhase("nacht", "Tiefschlaf", 0, 4))
DayPhaseStore.add(DayPhase("dunkel", "Frühe Dunkelheit", 4, 6))
DayPhaseStore.add(DayPhase("morgen", "Morgen", 6, 9))
DayPhaseStore.add(DayPhase("vormittag", "Vormittag", 9, 12))
DayPhaseStore.add(DayPhase("mittag", "Mittag", 12, 14))
DayPhaseStore.add(DayPhase("nachmittag", "Nachmittag", 14, 17))
DayPhaseStore.add(DayPhase("abend", "Abend", 17, 20))
DayPhaseStore.add(DayPhase("dämmerung", "Dämmerung", 20, 22))
DayPhaseStore.add(DayPhase("nacht2", "Späte Nacht", 22, 24))
