from typing import Callable

from yakoon.domains.game.models.character import Character
from yakoon.domains.game.models.room import Room
from yakoon.domains.game.stores.character_store import CharacterStore
from yakoon.domains.game.stores.room_store import RoomStore


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
        character.on_store_character: Callable[[Character], None] = CharacterStore.persist # type: ignore
        character.on_load_room: Callable[[str], Room] = RoomStore.get_by_id # type: ignore
