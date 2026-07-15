"""List all contacts."""

from y5n.sdk import ports

svc = ports.get("crm.contact.service")
ns = ports.get("crm.namespaces").contact_namespace()
all_contacts = svc.list_contacts(namespace=ns)

if not all_contacts:
    print("No contacts.")
else:
    print(f"Contacts ({len(all_contacts)}):")  # type: ignore
    print()
    for c in all_contacts:  # type: ignore
        parts = [f"  {c.data.name}"]
        if c.data.company:
            parts.append(f" - {c.data.company}")
        print("".join(parts))
