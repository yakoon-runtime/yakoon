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

from ..models import (
    PermissionGrant,
    PermissionGrantData,
)

# ----------------------------------
# INDEX
# ----------------------------------

IDX_GRANT_SUBJECT_KEY = IndexKey("grant.subject_key")

IDX_GRANT_SUBJECT_SPEC = IndexSpec(
    key=IDX_GRANT_SUBJECT_KEY,
    value_type=ValueType.TEXT,
    unique=False,
)

IDX_GRANT_PATH = IndexKey("grant.path")

IDX_GRANT_PATH_SPEC = IndexSpec(
    key=IDX_GRANT_PATH,
    value_type=ValueType.TEXT,
    unique=False,
)

# ----------------------------------
# SERVICE
# ----------------------------------


class PermissionGrantService:

    @staticmethod
    def index_specs():
        return [
            IDX_GRANT_SUBJECT_SPEC,
            IDX_GRANT_PATH_SPEC,
        ]

    def __init__(
        self,
        on_get: OnGet,
        on_append: OnAppend,
        on_replace: OnReplace,
        on_get_many: OnGetMany,
        on_scan: OnScan,
    ):
        self.on_get = on_get
        self.on_append = on_append
        self.on_replace = on_replace
        self.on_get_many = on_get_many
        self.on_scan = on_scan

    # ----------------------------------
    # API
    # ----------------------------------

    async def get_by_key(
        self,
        key: Key,
    ) -> PermissionGrant | None:

        row = await self.on_get(key=key)

        if not row.ok:
            return None

        return PermissionGrant.from_row(row=row)

    async def get_by_subject_and_path(
        self,
        *,
        namespace: Namespace,
        subject_key: Key,
        path: str,
    ) -> PermissionGrant | None:

        key = PermissionGrant.build_key(
            namespace=namespace,
            subject_key=subject_key,
            path=path,
        )

        return await self.get_by_key(key)

    async def list_grants(
        self,
        *,
        namespace: Namespace,
    ) -> list[PermissionGrant]:

        keys, _ = await self.on_scan(
            namespace=namespace,
            index_key=IDX_GRANT_SUBJECT_KEY,
        )

        rows = await self.on_get_many(keys=keys)

        grants = [PermissionGrant.from_row(row) for row in rows if row.ok]

        return [g for g in grants if g.data.enabled]

    async def list_subject_grants(
        self,
        *,
        namespace: Namespace,
        subject_key: Key,
    ) -> list[PermissionGrant]:

        keys, _ = await self.on_scan(
            namespace=namespace,
            index_key=IDX_GRANT_SUBJECT_KEY,
            value=str(subject_key),
        )

        rows = await self.on_get_many(keys=keys)

        grants = [PermissionGrant.from_row(row) for row in rows if row.ok]

        return [g for g in grants if g.data.enabled]

    async def list_path_grants(
        self,
        *,
        namespace: Namespace,
        path: str,
    ) -> list[PermissionGrant]:

        keys, _ = await self.on_scan(
            namespace=namespace,
            index_key=IDX_GRANT_PATH,
            value=path,
        )

        rows = await self.on_get_many(keys=keys)

        grants = [PermissionGrant.from_row(row) for row in rows if row.ok]

        return [g for g in grants if g.data.enabled]

    # ----------------------------------
    # STORAGE
    # ----------------------------------

    async def save(
        self,
        grant: PermissionGrant,
    ) -> None:

        doc = grant.data.to_dict()

        subject_key = doc.get("subject_key")
        path = doc.get("path")

        if not isinstance(subject_key, str):
            raise TypeError("PermissionGrant.subject_key " "must be a string")

        if not isinstance(path, str):
            raise TypeError("PermissionGrant.path " "must be a string")

        await self.on_replace(
            key=grant.key,
            doc=doc,
            indexes=[
                IndexTerm(
                    key=IDX_GRANT_SUBJECT_KEY,
                    value=subject_key,
                ),
                IndexTerm(
                    key=IDX_GRANT_PATH,
                    value=path,
                ),
            ],
            snapshot_hint=SnapshotHint.COMMIT,
        )

    # ----------------------------------
    # COMMANDS
    # ----------------------------------

    async def add_grant(
        self,
        *,
        namespace: Namespace,
        subject_key: Key,
        path: str,
        bits: str = "x",
        deny: bool = False,
    ) -> PermissionGrant:

        key = PermissionGrant.build_key(
            namespace=namespace,
            subject_key=subject_key,
            path=path,
        )

        grant = PermissionGrant(
            key=key,
            data=PermissionGrantData(
                subject_key=subject_key,
                path=path,
                bits=bits,
                deny=deny,
                enabled=True,
            ),
        )

        await self.save(grant)

        return grant

    async def remove_grant(
        self,
        *,
        namespace: Namespace,
        subject_key: Key,
        path: str,
    ) -> PermissionGrant:

        grant = await self.get_by_subject_and_path(
            namespace=namespace,
            subject_key=subject_key,
            path=path,
        )

        if not grant:
            raise ValueError("Permission grant not found")

        grant.data.enabled = False

        await self.save(grant)

        return grant
