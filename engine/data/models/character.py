from dataclasses import dataclass

@dataclass
class Character:
    id: str = ""
    name: str = ""
    location: str = "" # room_id