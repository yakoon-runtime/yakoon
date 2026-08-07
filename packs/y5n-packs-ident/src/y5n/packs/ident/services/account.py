from __future__ import annotations

from y5n.runtime.api.naming import Key, Namespace
from y5n.runtime.store.event.models import (
    IndexKey,
    IndexSpec,
    IndexTerm,
    SnapshotHint,
    ValueType,
)
from y5n.runtime.store.event.ports import (
    OnAppend,
    OnGet,
    OnGetMany,
    OnReplace,
    OnScan,
)

from ..models import Account, AccountData

# ----------------------------------
# INDEX
# ----------------------------------

IDX_ACCOUNT_USERNAME_KEY = IndexKey("account.username")
IDX_ACCOUNT_USERNAME_SPEC = IndexSpec(
    key=IDX_ACCOUNT_USERNAME_KEY,
    value_type=ValueType.TEXT,
    unique=True,
)


class AccountService:
    """
    Loads/saves accounts via ES-light EntityStore.
    An account is the login identity inside a runtime; it owns
    credentials, groups, and grants (permission carrier).
    """

    @staticmethod
    def index_specs():
        return [IDX_ACCOUNT_USERNAME_SPEC]

    def __init__(
        self,
        on_append: OnAppend,
        on_replace: OnReplace,
        on_get_by_key: OnGet,
        on_get_many: OnGetMany,
        on_scan: OnScan,
    ):
        self.on_append = on_append
        self.on_replace = on_replace
        self.on_get_by_key = on_get_by_key
        self.on_get_many = on_get_many
        self.on_scan = on_scan

    async def get_by_key(self, key: Key) -> Account | None:
        row = await self.on_get_by_key(key=key)
        if not row.ok:
            return None

        return Account.from_row(row=row)

    async def get_by_username(
        self, namespace: Namespace, username: str
    ) -> Account | None:

        keys, _ = await self.on_scan(
            namespace=namespace,
            index_key=IDX_ACCOUNT_USERNAME_KEY,
            value=username,
            limit=1,
        )

        if not keys:
            return None

        row = await self.on_get_by_key(key=keys[0])
        if not row.ok:
            return None

        return Account.from_row(row=row)

    async def list_accounts(self, namespace: Namespace) -> list[Account]:
        keys, _ = await self.on_scan(
            namespace=namespace,
            index_key=IDX_ACCOUNT_USERNAME_KEY,
        )

        rows = await self.on_get_many(keys=keys)
        accounts = [Account.from_row(row) for row in rows if row.ok]

        return [a for a in accounts if a.data.enabled]

    async def save(self, account: Account) -> None:
        key = account.key
        doc = account.data.to_dict()

        username = doc.get("username")
        if not isinstance(username, str):
            raise TypeError("Account.username must be a string")

        await self.on_replace(
            key=key,
            doc=doc,
            indexes=[IndexTerm(key=IDX_ACCOUNT_USERNAME_KEY, value=username)],
            snapshot_hint=SnapshotHint.COMMIT,
        )

    async def add_account(
        self,
        *,
        namespace: Namespace,
        username: str,
        password: str | None = None,
        name: str | None = None,
        mail: str | None = None,
        language: str | None = None,
    ) -> Account:
        key = Key(namespace=namespace, id=username)

        existing = await self.get_by_key(key)
        if existing:
            raise ValueError(f"Account already exists: {username}")

        account = Account(
            key=key,
            data=AccountData(
                username=username,
                password_hash=password,
                name=name,
                mail=mail,
                language=language,
            ),
        )

        await self.save(account)
        return account

    async def edit_account(
        self,
        *,
        namespace: Namespace,
        username: str,
        changes: dict,
    ) -> Account:
        account = await self.get_by_username(namespace, username)
        if not account:
            raise ValueError(f"Account not found: {username}")

        password = changes.get("password")
        if password is not None:
            account.data.password_hash = password

        enabled = changes.get("enabled")
        if enabled is not None:
            account.data.enabled = enabled

        for field in ("name", "mail", "language"):
            value = changes.get(field)
            if value is not None:
                setattr(account.data, field, value)

        await self.save(account)
        return account

    async def delete_by_username(
        self,
        *,
        namespace: Namespace,
        username: str,
    ) -> None:
        account = await self.get_by_username(namespace, username)
        if not account:
            raise ValueError(f"Account not found: {username}")

        account.data.enabled = False
        await self.save(account)

    async def delete_by_key(self, key: Key) -> None:
        account = await self.get_by_key(key)
        if not account:
            raise ValueError(f"Account not found: {key}")

        account.data.enabled = False
        await self.save(account)
