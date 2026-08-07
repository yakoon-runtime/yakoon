# services/permissions/resolver.py

from __future__ import annotations

from typing import Protocol

from y5n.runtime.api.naming import Key, Namespace

from ..models import Join, PermissionGrant


class PermissionResolver:
    """Resolves an account's effective permissions to spec strings.

    The pack owns the sources (direct grants, group grants). The result
    is a list of serializable spec strings (e.g. "/crm/contact/edit|rwx",
    "-/crm/contact/edit|x") that the engine parses into a PermissionSet.
    """

    def __init__(
        self,
        on_list_account_joins: OnListAccountJoins,
        on_list_subject_grants: OnListSubjectGrants,
    ):
        self.on_list_account_joins = on_list_account_joins
        self.on_list_subject_grants = on_list_subject_grants

    # ----------------------------------
    # RESOLVE
    # ----------------------------------

    async def resolve_account_permissions(
        self,
        *,
        grant_namespace: Namespace,
        join_namespace: Namespace,
        account_key: Key,
    ) -> list[str]:

        out: list[str] = []

        direct_grants = await self.on_list_subject_grants(
            namespace=grant_namespace,
            subject_key=account_key,
        )

        self._merge_grants(out, direct_grants)

        joins = await self.on_list_account_joins(
            namespace=join_namespace,
            account_key=account_key,
        )

        for join in joins:
            grants = await self.on_list_subject_grants(
                namespace=grant_namespace,
                subject_key=(join.group_key),
            )

            self._merge_grants(out, grants)

        return out

    # ----------------------------------
    # INTERNAL
    # ----------------------------------

    @staticmethod
    def _merge_grants(
        target: list[str],
        grants: list[PermissionGrant],
    ):
        for grant in grants:
            spec = f"{grant.permission_key}|{grant.bits}"
            if grant.deny:
                spec = f"-{spec}"

            target.append(spec)


# ----------------------------------
# PORTS
# ----------------------------------


class OnListAccountJoins(Protocol):
    async def __call__(
        self,
        *,
        namespace: Namespace,
        account_key: Key,
    ) -> list[Join]: ...


class OnListSubjectGrants(Protocol):
    async def __call__(
        self,
        *,
        namespace: Namespace,
        subject_key: Key,
    ) -> list[PermissionGrant]: ...
