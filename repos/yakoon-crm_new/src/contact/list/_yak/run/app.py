"""Yakoon Standard Command — list all contacts.

Copyright 2024 Yakoon. Apache 2.0 license.
Part of the Yakoon CRM reference implementation.
"""

from collections.abc import Sequence
from typing import Protocol

from y5n.base.naming import Namespace
from y5n.sdk import ports


class ContactData(Protocol):
    """Shape of a contact's data object (from crm service)."""
    name: str
    company: str
    email: str
    phone: str


class Contact(Protocol):
    """Shape of a contact object returned by the CRM service."""
    data: ContactData


class ContactService(Protocol):
    """Local protocol for the CRM contact service port.

    Defines which methods the service exposes. Used by the
    type checker and IDE — zero runtime overhead.
    """
    def list_contacts(self, namespace: Namespace) -> Sequence[Contact]: ...
    def get_by_name(self, namespace: Namespace, name: str) -> Contact | None: ...
    def add_contact(self, namespace: Namespace, name: str, **kw: str) -> Contact: ...
    def edit_contact(self, namespace: Namespace, name: str, changes: dict) -> Contact: ...
    def delete_contact(self, namespace: Namespace, name: str) -> None: ...


def main():
    """Command entry point.

    A def main() is a structural convention, not a requirement.
    Yakoon commands can be written as simple scripts without it.

    If you need async (e.g. for timers, external APIs):

        async def main():
            ...
            result = await async_function()
            ...

        asyncio.run(main())

    The transport handles async provider methods transparently —
    you can call await or not, both work.
    """
    svc: ContactService = ports.get("crm.contact.service")
    ns = ports.get("crm.namespaces").contact_namespace()
    all_contacts = svc.list_contacts(namespace=ns)

    if not all_contacts:
        print("No contacts.")
    else:
        print(f"Contacts ({len(all_contacts)}):")
        print()
        for c in all_contacts:
            parts = [f"  {c.data.name}"]
            if c.data.company:
                parts.append(f" - {c.data.company}")
            print("".join(parts))


main()
