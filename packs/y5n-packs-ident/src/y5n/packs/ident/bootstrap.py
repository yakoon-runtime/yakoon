from y5n.runtime.api.naming import Key

from .models import (
    Account,
    AccountData,
    Group,
    GroupData,
    Join,
    JoinData,
    PermissionGrant,
    PermissionGrantData,
)
from .services import (
    AccountService,
    GroupService,
    JoinService,
    Namespaces,
    PermissionGrantService,
)

_root_grant_specs = [
    "/ident/accounts|rwx",
    "/ident/groups|rwx",
    "/ident/joins|rwx",
    "/ident/grants|rwx",
]


async def bootstrap(
    accounts: AccountService,
    groups: GroupService,
    join_svc: JoinService,
    permgrant: PermissionGrantService,
) -> None:

    namespaces = Namespaces()

    account_ns = namespaces.account_namespace()
    group_ns = namespaces.group_namespace()
    join_ns = namespaces.join_namespace()
    grant_ns = namespaces.permgrant_namespace()

    # -------------------
    # --- ROOT / ADMIN ---
    # -------------------

    root_account_key = Key(
        namespace=account_ns,
        id="root",
    )

    admins_key = Key(
        namespace=group_ns,
        id="admins",
    )

    # -----------------------
    # --- ROOT ACCOUNT ---
    # -----------------------

    if not await accounts.get_by_key(root_account_key):
        await accounts.save(
            Account(
                key=root_account_key,
                data=AccountData(
                    username="root",
                    password_hash="master",
                ),
            )
        )

    # -----------------------
    # --- ADMINS GROUP ---
    # -----------------------

    if not await groups.get_by_key(admins_key):
        await groups.save(
            Group(
                key=admins_key,
                data=GroupData(
                    name="admins",
                ),
            )
        )

    # -----------------------
    # --- ROOT MEMBERSHIP ---
    # -----------------------

    join_key = Join.build_key(
        namespace=join_ns,
        account_key=root_account_key,
        group_key=admins_key,
    )

    if not await join_svc.get_by_key(join_key):
        await join_svc.save(
            Join(
                key=join_key,
                data=JoinData(
                    account_key=root_account_key,
                    group_key=admins_key,
                ),
            )
        )

    # -------------------
    # --- ROOT GRANTS ---
    # -------------------

    for spec in _root_grant_specs:

        grant_key = PermissionGrant.build_key(
            namespace=grant_ns,
            subject_key=admins_key,
            permission_key=spec,
        )

        if await permgrant.get_by_key(grant_key):
            continue

        await permgrant.save(
            PermissionGrant(
                key=grant_key,
                data=PermissionGrantData(
                    subject_key=admins_key,
                    permission_key=spec,
                ),
            )
        )
