from __future__ import annotations

from y5n.runtime.api.naming import Key
from y5n.runtime.store.event.wire import build_store
from y5n.sdk import ports

from .bootstrap import bootstrap
from .models import Account, AccountData
from .services import (
    AccountService,
    AllowAllSecretVerifier,
    AuthenticationService,
    GroupService,
    JoinService,
    Namespaces,
    PermissionGrantService,
    PermissionResolver,
)
from .settings import Settings


async def main():

    settings = Settings()
    store = build_store(settings.storage)
    await _build_index(store)

    service_ns = Namespaces()

    accounts = AccountService(
        on_append=store.objects.append,
        on_replace=store.objects.replace,
        on_get_by_key=store.objects.get,
        on_get_many=store.objects.get_many,
        on_scan=store.objects.scan,
    )

    groups = GroupService(
        on_get=store.objects.get,
        on_append=store.objects.append,
        on_replace=store.objects.replace,
        on_get_many=store.objects.get_many,
        on_scan=store.objects.scan,
    )

    join_svc = JoinService(
        on_get=store.objects.get,
        on_append=store.objects.append,
        on_replace=store.objects.replace,
        on_get_many=store.objects.get_many,
        on_scan=store.objects.scan,
    )

    permgrant = PermissionGrantService(
        on_get=store.objects.get,
        on_append=store.objects.append,
        on_replace=store.objects.replace,
        on_get_many=store.objects.get_many,
        on_scan=store.objects.scan,
    )

    resolver = PermissionResolver(
        on_list_account_joins=join_svc.list_account_joins,
        on_list_subject_grants=permgrant.list_subject_grants,
    )

    verifier = AllowAllSecretVerifier()

    async def on_after_verify(*, account) -> dict:
        return {}

    auth = AuthenticationService(
        on_get_account=accounts.get_by_username,
        on_verify_account=verifier.verify,
        on_resolve_permissions=resolver.resolve_account_permissions,
        on_after_verify=on_after_verify,
        namespace=service_ns.account_namespace(),
    )

    await bootstrap(
        accounts=accounts,
        groups=groups,
        join_svc=join_svc,
        permgrant=permgrant,
    )

    await _demo_data(accounts=accounts)

    # ---------------
    # --- PUBLISH ---
    # ---------------

    ports.publish("ident.accounts", accounts)
    ports.publish("ident.namespaces", service_ns)
    ports.publish("ident.groups", groups)
    ports.publish("ident.joins", join_svc)
    ports.publish("ident.permgrant", permgrant)
    ports.publish("ident.permissions.resolver", resolver)

    # ---------------
    # --- PROMOTE ---
    # ---------------

    ports.promote("ident.auth", auth)


async def _build_index(store):
    namespaces = Namespaces()
    await store.objects.ensure_indexes(
        namespace=namespaces.account_namespace(),
        specs=AccountService.index_specs(),
    )
    await store.objects.ensure_indexes(
        namespace=namespaces.group_namespace(),
        specs=GroupService.index_specs(),
    )
    await store.objects.ensure_indexes(
        namespace=namespaces.join_namespace(),
        specs=JoinService.index_specs(),
    )
    await store.objects.ensure_indexes(
        namespace=namespaces.permgrant_namespace(),
        specs=PermissionGrantService.index_specs(),
    )


async def _demo_data(accounts) -> None:
    namespaces = Namespaces()
    account_ns = namespaces.account_namespace()

    a1 = Account(
        key=Key(namespace=account_ns, id="stefan"),
        data=AccountData(
            username="stefan",
            password_hash="123",
            name="Stefan Bergmann",
            language="de",
        ),
    )
    await accounts.save(a1)

    a2 = Account(
        key=Key(namespace=account_ns, id="lara"),
        data=AccountData(
            username="lara",
            password_hash="456",
            name="Lara",
            language="de",
        ),
    )
    await accounts.save(a2)
