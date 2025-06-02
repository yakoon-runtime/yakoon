
from yakoon.models.namespace import Namespace
from yakoon.domains.realm.models.character import Character


class InMemoryCharacterStore:
    
    def __init__(self):
        self._chars: dict[str, Character] = {}
        load_defaults(self)

    async def create(self, ns: Namespace, char: Character):
        char.validate()
        self._chars[ns.get_key(char.id)] = char

    async def get_by_id(self, ns: Namespace, id_: str) -> Character | None:
        return self._chars.get(ns.get_key(id_))

    async def get_by_name(self, ns: Namespace, name: str) -> list[Character]:
        for k, v, in self._chars.items():
            if name and name.lower() == v.name.lower():
                return v

    def add(self, ns: Namespace, char: Character):
        char.validate()
        self._chars[ns.get_key(char.id)] = char


def load_defaults(store: InMemoryCharacterStore):

    ns = Namespace(domain="realm", bucket="bucket", scope="develop")

    store.add(ns,
        Character(id="char-stefan", name="Stefan", location="forest"))
    store.add(ns,
        Character(id="char-lara", name="Lara", location="hall"))