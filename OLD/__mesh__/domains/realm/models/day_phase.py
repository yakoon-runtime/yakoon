
from dataclasses import dataclass


@dataclass
class DayPhase:
    id: str                # z. B. "morgen"
    name: str              # z. B. "Morgen"
    start_hour: int        # inklusiv
    end_hour: int          # exklusiv
    description: str = ""  # optional

    def validate(self):
        pass