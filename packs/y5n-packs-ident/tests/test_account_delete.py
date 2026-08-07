"""account delete — an account cannot delete its own identity.

The rule is generic, not name-based: "an account must not delete its own
identity." Deleting another account works; deleting yourself renders the
`denied` variant and leaves the account intact.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from y5n.runtime.api.runtime.context import set_context
from y5n.runtime.engine.runtime.invocation import (
    derive_invocation_context,
    establish_invocation_context,
)


@pytest.fixture(autouse=True)
def _sdk_endpoint(monkeypatch):
    monkeypatch.setenv("YAK_ENDPOINT", "inprocess://")
    from y5n.sdk import ports

    yield ports


class _Services:
    def __init__(self):
        self.rendered: list[tuple[str, dict]] = []
        self.deleted: list[str] = []


def _services(ports, monkeypatch):
    services = _Services()

    document = AsyncMock()
    document.render = AsyncMock(
        side_effect=lambda name, state: services.rendered.append((name, state))
        or f"<{name}>"
    )
    ports.publish("document", document)

    ns = AsyncMock()
    ns.account_namespace = AsyncMock(return_value="realm/account/global")
    ports.publish("ident.namespaces", ns)

    accounts = AsyncMock()
    accounts.delete_by_username = AsyncMock(
        side_effect=lambda *, namespace, username: services.deleted.append(username)
    )
    ports.publish("ident.accounts", accounts)

    from y5n.sdk import io as sdk_io

    monkeypatch.setattr(sdk_io, "write", AsyncMock())

    return services


def _run(username: str, me: str | None):
    from y5n.packs.ident.apps.accounts import delete as delete_cmd

    class _FakeNode:
        key = "delete"
        path = "/usr/sbin/ident/account/delete"

    async def _driver():
        ctx = derive_invocation_context(
            node=_FakeNode(),
            session=None,
            flow_id="t",
            tokens=[username],
        )
        if me is not None:
            ctx["user"] = {"id": "realm/account/global#a-1", "name": me}
        establish_invocation_context(ctx)
        await delete_cmd.main()

    return _driver


@pytest.mark.asyncio
async def test_delete_own_account_is_denied(_sdk_endpoint, monkeypatch):
    services = _services(_sdk_endpoint, monkeypatch)

    await _run("stefan", me="stefan")()

    assert services.rendered == [("denied", {"name": "stefan"})]
    assert services.deleted == []


@pytest.mark.asyncio
async def test_delete_other_account_succeeds(_sdk_endpoint, monkeypatch):
    services = _services(_sdk_endpoint, monkeypatch)

    await _run("lara", me="stefan")()

    assert services.rendered == [("default", {"name": "lara"})]
    assert services.deleted == ["lara"]


@pytest.mark.asyncio
async def test_delete_without_identity_is_allowed(_sdk_endpoint, monkeypatch):
    """Anonymous / unattached sessions can still delete (no self-reference)."""
    services = _services(_sdk_endpoint, monkeypatch)

    await _run("lara", me=None)()

    assert services.deleted == ["lara"]
