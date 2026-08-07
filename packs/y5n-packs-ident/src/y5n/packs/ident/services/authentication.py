from __future__ import annotations

from typing import Protocol

from y5n.runtime.api.naming import Key, Namespace
from y5n.runtime.api.ports.protocols import OnAfterVerify
from y5n.sdk import ports

from ..models import Account


class AuthenticationService:

    def __init__(
        self,
        on_get_account: OnGetAccount,
        on_verify_account: OnVerifyAccount,
        on_resolve_permissions: OnResolvePermissions,
        on_after_verify: OnAfterVerify,
        namespace: Namespace,
    ):
        self.on_get_account = on_get_account
        self.on_verify = on_verify_account
        self.on_resolve_permissions = on_resolve_permissions
        self.on_after_verify = on_after_verify
        self._namespace = namespace

    async def authenticate(
        self,
        *,
        username: str,
        secret: str,
        security_context: str = "normal",
    ) -> dict:

        account = await self.on_get_account(
            namespace=self._namespace, username=username
        )
        if not account:
            return {"ok": False, "reason": "unknown-account"}

        if not account.is_active():
            return {"ok": False, "reason": "account-disabled"}

        if not self.on_verify(account=account, secret=secret):
            return {"ok": False, "reason": "invalid-credentials"}

        after = await self.on_after_verify(account=account)

        ses = ports.get("session")
        await ses.update(
            patch={
                "user_key": str(account.key),
                "user_name": account.username,
                "security_context": security_context,
            }
        )

        specs = await self.on_resolve_permissions(account_key=account.key)
        await ses.set_permissions(specs=specs)

        return {
            "ok": True,
            "user": self._to_dict(account),
            "permissions": specs,
            "after": after,
        }

    async def logout(self) -> None:
        ses = ports.get("session")
        await ses.logout()

    def _to_dict(self, account: Account) -> dict:
        return {
            "key": account.key,
            "username": account.username,
        }


# ----------------------------------
# PORTS
# ----------------------------------


class OnGetAccount(Protocol):
    async def __call__(
        self,
        *,
        namespace: Namespace,
        username: str,
    ) -> Account | None: ...


class OnVerifyAccount(Protocol):
    def __call__(
        self,
        *,
        account: Account,
        secret: str,
    ) -> bool: ...


class OnResolvePermissions(Protocol):
    async def __call__(
        self,
        *,
        account_key: Key,
    ) -> list[str]: ...
