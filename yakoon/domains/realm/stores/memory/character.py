
from typing import Optional
from yakoon.models.key import Key
from yakoon.models.namespace import Namespace
from yakoon.domains.realm.models.character import Character
from yakoon.stores.memory.base_store import MemoryStore


class InMemoryCharacterStore(MemoryStore):
    """
    Domain-specific store for BaseSession objects.
    Currently uses raw MemoryStore behavior.
    Override methods here only if session-specific logic is required.
    """

    def __init__(self):
        super().__init__()
        load_defaults(self)

    def add(self, char: Character):
        self._rows[str(char.key)] = char.to_row()


def load_defaults(store: InMemoryCharacterStore):

    ns = Namespace(domain="yakoon", bucket="bucket", scope="develop")

    store.add(Character(
        key=Key(namespace=ns, id="char-stefan"),
        name="Stefan",location="forest"))

    store.add(Character(
        key=Key(namespace=ns, id="char-lara"),
        name="Lara",location="hall"))
