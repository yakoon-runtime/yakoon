from typing import Optional
from yakoon.saas.controllers.gateway.models.account import Account
from yakoon.mesh.models.key import Key
from yakoon.mesh.models.namespace import Namespace
from yakoon.mesh.stores.memory.base_store import MemoryStore


class InMemoryAccountStore(MemoryStore):
    """
    Domain-specific store for BaseSession objects.
    Currently uses raw MemoryStore behavior.
    Override methods here only if session-specific logic is required.
    """

    def __init__(self):
        super().__init__()

    def __init__(self):
        super().__init__()
        load_defaults(self)

    def add(self, account: Account): 
        self._rows[str(account.key)] = account.to_row()


def load_defaults(store: InMemoryAccountStore):
    ns = Namespace(domain="yakoon", bucket="bucket", scope="develop")

    store.add(Account(
        key=Key(namespace=ns, id="acc-stefan"),
        name="Stefan",
        cmd_groups=["realm:system", "realm:account", "realm:character"]
    ))

    store.add(Account(
        key=Key(namespace=ns, id="acc-lara"),
        name="Lara",
        cmd_groups=["system"]
    ))
