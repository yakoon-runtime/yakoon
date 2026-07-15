"""Yakoon Standard Command — list all contacts.

Copyright 2024 Yakoon. Apache 2.0 license.
Part of the Yakoon CRM reference implementation.
"""

from y5n.sdk import ports


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
    svc = ports.get("crm.contact.service")
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
