
from yakoon.models.key import Key


class Namespace:
    """
    Represents a namespaced identifier context for addressing objects.

    Components:
    - domain: The functional domain or module (e.g., 'realm', 'minddojo')
    - bucket: A specific collection or world scope (e.g., 'dojo-42', 'session-abc')
    - scope: An optional isolation context (e.g., 'global', 'user:xyz', 'tenant:abc')

    Together, these define a unique namespace used for ID resolution, scoping, and separation.
    """

    def __init__(self, domain: str, bucket: str, scope: str = "global"):
        self.domain = domain
        self.bucket = bucket
        self.scope = scope

    def get_prefix(self) -> str:
        return f"{self.domain}:{self.bucket}:{self.scope}"

    def get_key(self, id: str) -> Key:
        return Key(self, id)
    
    def __eq__(self, other):
        return (
            isinstance(other, Namespace)
            and self.domain == other.domain
            and self.bucket == other.bucket
            and self.scope == other.scope
        )

    def __hash__(self):
        return hash((self.domain, self.bucket, self.scope))
