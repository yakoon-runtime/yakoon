from typing import Dict, Optional
from mygame.models.character import Character

# Beispiel-Datenbank
CHARACTERS: Dict[str, Character] = {
    "stefan": Character(id="stefan", name="Stefan", location="forest"),
    "lara": Character(id="lara", name="Lara", location="hall"),
}

class CharacterStore:
    @staticmethod
    def get(char_id: str) -> Optional[Character]:
        return CHARACTERS.get(char_id)

    @staticmethod
    def all() -> list[Character]:
        return list(CHARACTERS.values())

    @staticmethod
    def exists(char_id: str) -> bool:
        return char_id in CHARACTERS
