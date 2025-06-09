from dataclasses import dataclass


@dataclass
class Season:
    id: str              # z. B. "winter"
    name: str            # z. B. "Winter"
    start_day: int       # z. B. 270
    end_day: int         # z. B. 359

    def validate(self):
        pass