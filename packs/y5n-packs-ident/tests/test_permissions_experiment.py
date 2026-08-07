"""End-to-end experiment test: permissions are granted to accounts on runtime paths.

Covers the full pipeline without process boundaries:
  store -> services -> bootstrap -> resolver -> parser -> PermissionSet -> check
"""

from __future__ import annotations

import pytest
from y5n.packs.ident.bootstrap import bootstrap
from y5n.packs.ident.services import (
    AccountService,
    GroupService,
    JoinService,
    Namespaces,
    PermissionGrantService,
    PermissionResolver,
)
from y5n.runtime.api.naming import Key
from y5n.runtime.engine.capabilities.permission import (
    PermissionParser,
    PermissionSet,
)
from y5n.runtime.store.event.settings import StorageSettings
from y5n.runtime.store.event.wire import build_store


@pytest.fixture
async def services():
    store = build_store(StorageSettings())
    await store.initialize()

    ns = Namespaces()
    await store.objects.ensure_indexes(
        namespace=ns.account_namespace(), specs=AccountService.index_specs()
    )
    await store.objects.ensure_indexes(
        namespace=ns.group_namespace(), specs=GroupService.index_specs()
    )
    await store.objects.ensure_indexes(
        namespace=ns.join_namespace(), specs=JoinService.index_specs()
    )
    await store.objects.ensure_indexes(
        namespace=ns.permgrant_namespace(), specs=PermissionGrantService.index_specs()
    )

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
    joins = JoinService(
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
        grant_namespace=ns.permgrant_namespace(),
        join_namespace=ns.join_namespace(),
        on_list_account_joins=joins.list_account_joins,
        on_list_subject_grants=permgrant.list_subject_grants,
    )

    await bootstrap(
        accounts=accounts,
        groups=groups,
        join_svc=joins,
        permgrant=permgrant,
    )

    return {
        "ns": ns,
        "accounts": accounts,
        "groups": groups,
        "joins": joins,
        "permgrant": permgrant,
        "resolver": resolver,
    }


async def _effective(svcs, account_key: Key) -> PermissionSet:
    specs = await svcs["resolver"].resolve_account_permissions(
        account_key=account_key,
    )
    parser = PermissionParser()
    permset = PermissionSet()
    for spec in specs:
        permset.add(parser.parse(spec))
    return permset


@pytest.mark.asyncio
async def test_root_account_gets_admin_group_permissions(services):
    account = await services["accounts"].get_by_username(
        namespace=services["ns"].account_namespace(), username="root"
    )
    assert account is not None

    permset = await _effective(services, account.key)

    # root grant covers the whole tree via inheritance
    assert permset.check("/", "rwx")
    assert permset.check("/usr/bin/ls", "x")
    assert permset.check("/usr/sbin/ident/accounts", "rwx")
    assert permset.check("/opt/crm", "rwx")
    assert permset.check("/dsl", "rwx")
    assert permset.check("/boot", "r")


@pytest.mark.asyncio
async def test_root_deny_grant_subtracts_group_allow(services):
    account = await services["accounts"].get_by_username(
        namespace=services["ns"].account_namespace(), username="root"
    )
    await services["permgrant"].add_grant(
        namespace=services["ns"].permgrant_namespace(),
        subject_key=account.key,
        path="/usr/bin",
        bits="x",
        deny=True,
    )

    permset = await _effective(services, account.key)

    assert not permset.check("/usr/bin/shutdown", "x")
    assert permset.check("/usr/bin/ls", "r")
    assert permset.check("/usr/sbin/ident/accounts", "rwx")


@pytest.mark.asyncio
async def test_new_account_without_grants_has_no_permissions(services):
    account = await services["accounts"].add_account(
        namespace=services["ns"].account_namespace(),
        username="guest",
        password="pw",
    )

    permset = await _effective(services, account.key)

    assert not permset.check("/usr/bin/ls", "x")
    assert not permset.check("/usr/sbin/ident", "rwx")
