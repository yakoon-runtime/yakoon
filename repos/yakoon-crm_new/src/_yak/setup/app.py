"""CRM setup — registers contact service in the runtime."""

from y5n.sdk import ports
from y5nstore.event.wire import build_store
from y5nstore.sequence.wire import build_store as build_sequencer

from .services import ContactService, Namespaces
from .settings import Settings


async def run(space):
    settings = Settings.load()
    namespaces = Namespaces()
    store = build_store(settings.storage)
    sequencer = build_sequencer(settings.sequencer)
    await sequencer.initialize()

    for spec in ContactService.index_specs():
        await store.objects.ensure_indexes(
            namespace=namespaces.contact_namespace(),
            specs=[spec],
        )

    contacts = ContactService(
        on_get=store.objects.get,
        on_replace=store.objects.replace,
        on_get_many=store.objects.get_many,
        on_scan=store.objects.scan,
        on_delete=store.objects.delete,
        on_query_index=store.objects.query_index,
        on_next_id=sequencer.next_id,
    )

    ports.register(
        "crm.contact.service",
        {
            "list_contacts": contacts.list_contacts,
            "get_by_name": contacts.get_by_name,
            "add_contact": contacts.add_contact,
            "edit_contact": contacts.edit_contact,
            "delete_contact": contacts.delete_contact,
            "find_contacts": contacts.find_contacts,
        },
    )

    ports.register(
        "crm.namespaces",
        {
            "contact_namespace": namespaces.contact_namespace,
        },
    )

    print("crm: contact service registered")
