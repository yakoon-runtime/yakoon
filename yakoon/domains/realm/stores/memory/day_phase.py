from yakoon.domains.realm.models.day_phase import DayPhase


class InMemoryDayPhaseStore:
    
    def __init__(self):
        self._phases: list[DayPhase] = []
        load_defaults(self)

    def all(self) -> list[DayPhase]:
        return self._phases

    def add(self, phase: DayPhase):
        self._phases.append(phase)

    def clear(self):
        self._phases.clear()


def load_defaults(store: InMemoryDayPhaseStore):
    store.add(DayPhase("nacht", "Tiefschlaf", 0, 4))
    store.add(DayPhase("dunkel", "Frühe Dunkelheit", 4, 6))
    store.add(DayPhase("morgen", "Morgen", 6, 9))
    store.add(DayPhase("vormittag", "Vormittag", 9, 12))
    store.add(DayPhase("mittag", "Mittag", 12, 14))
    store.add(DayPhase("nachmittag", "Nachmittag", 14, 17))
    store.add(DayPhase("abend", "Abend", 17, 20))
    store.add(DayPhase("dämmerung", "Dämmerung", 20, 22))
    store.add(DayPhase("nacht2", "Späte Nacht", 22, 24))
