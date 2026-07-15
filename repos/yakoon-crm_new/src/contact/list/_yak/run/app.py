from y5n.sdk import ports


def main():

    svc = ports.get("crm.contact.service")
    ns = ports.get("crm.namespaces").contact_namespace()

    contacts = svc.list_contacts(namespace=ns)

    if not contacts:
        print("No contacts.")
        return

    print(f"Contacts ({len(contacts)}):")
    print()

    for c in contacts:
        parts = [f"  {c.data.name}"]
        if c.data.company:
            parts.append(f" - {c.data.company}")
        print("".join(parts))


main()
