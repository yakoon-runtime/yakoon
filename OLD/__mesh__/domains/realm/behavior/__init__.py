from typing import Callable

from yakoon.platform.domains.realm.models.character import Character
from yakoon.platform.domains.realm.models.room import Room
from yakoon.platform.domains.realm.services.character import CharacterService
from yakoon.platform.domains.realm.services.room import RoomService

class CharacterBehavior:
    """
    Attaches domain-specific behavior to a Character instance.
    Injects logic for persistence and room loading.
    """

    @staticmethod
    def attach(character: Character) -> None:
        """
        Injects store-dependent behavior into the given Character instance.
        This avoids circular imports and keeps the model clean.
        """
        character.on_store_character: Callable[[Character], None] = CharacterService.save # type: ignore
        character.on_load_room: Callable[[str], Room] = RoomService.get_by_id # type: ignore
