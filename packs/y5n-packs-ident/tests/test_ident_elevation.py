"""Elevation flow in the ident pack: login establishes the security context.

`su --administrative` and `su --temporary` are the will act — the password
is the confirmation. The AuthenticationService passes the requested
security context through to the session; the default login stays normal.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from y5n.packs.ident.services.authentication import AuthenticationService
from y5n.runtime.api.naming import Key, Namespace


@pytest.fixture(autouse=True)
def _sdk_endpoint(monkeypatch):
    monkeypatch.setenv("YAK_ENDPOINT", "inprocess://")
    from y5n.sdk import ports, security

    yield ports, security


def _account(username: str):
    from y5n.packs.ident.models import Account, AccountData

    return Account(
        key=Key.from_parts("test", "accounts", "global", f"a-{username}"),
        data=AccountData(username=username, password_hash="secret"),
    )


async def _authenticate(ports, **kwargs) -> dict:
    session = AsyncMock()
    session.update = AsyncMock(return_value={"applied": {}, "ignored": {}})
    session.set_permissions = AsyncMock(return_value={"granted": 0})
    ports.publish("session", session)

    def verify(*, account, secret) -> bool:
        return secret == account.data.password_hash

    auth = AuthenticationService(
        on_get_account=AsyncMock(return_value=_account("stefan")),
        on_verify_account=verify,
        on_resolve_permissions=AsyncMock(return_value=[]),
        on_after_verify=AsyncMock(return_value={}),
        namespace=Namespace("test", "account", "global"),
    )

    return await auth.authenticate(**kwargs), session


@pytest.mark.asyncio
async def test_login_defaults_to_normal_context(_sdk_endpoint):
    ports, security = _sdk_endpoint
    result, session = await _authenticate(ports, username="stefan", secret="secret")

    assert result["ok"] is True
    patch = session.update.await_args.kwargs["patch"]
    assert patch["security_context"] == security.SecurityContext.NORMAL


@pytest.mark.asyncio
async def test_administrative_login_sets_administrative_context(_sdk_endpoint):
    ports, security = _sdk_endpoint
    result, session = await _authenticate(
        ports,
        username="stefan",
        secret="secret",
        security_context=security.SecurityContext.ADMINISTRATIVE,
    )

    assert result["ok"] is True
    patch = session.update.await_args.kwargs["patch"]
    assert patch["security_context"] == security.SecurityContext.ADMINISTRATIVE


@pytest.mark.asyncio
async def test_temporary_login_sets_temporary_context(_sdk_endpoint):
    ports, security = _sdk_endpoint
    result, session = await _authenticate(
        ports,
        username="stefan",
        secret="secret",
        security_context=security.SecurityContext.TEMPORARY,
    )

    assert result["ok"] is True
    patch = session.update.await_args.kwargs["patch"]
    assert patch["security_context"] == security.SecurityContext.TEMPORARY
