from dataclasses import dataclass

@dataclass
class ClimateZone:
    id: str             # e.g. "desert", "alpine"
    name: str           # e.g. "Desert", "Alpine Zone"
    temperature: str    # e.g. "hot", "cold", "mild"
    humidity: str       # e.g. "dry", "humid"
    description: str = ""

    def validate(self):
        pass