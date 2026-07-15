"""Runtime Bus handlers — one per message type.

Each handler is a callable registered with the bus.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .context import Call, Response
from .messages import Ok, RegisterProvider, UnregisterProvider

if TYPE_CHECKING:
    from .resolver import Resolver
    from .transport import DirectTransport


class CallHandler:
    """Handles Call messages.

    Uses the Resolver to find a provider and the Transport to deliver.
    """

    def __init__(self, resolver: Resolver, transport: DirectTransport) -> None:
        self._resolver = resolver
        self._transport = transport

    def __call__(self, call: Call) -> Response:
        provider_id = self._resolver.resolve(
            call.port, call.method, caller_path=call.caller_path
        )
        if provider_id is None:
            return Response(error=f"no provider for '{call.port}:{call.method}'")
        return self._transport.send(provider_id, call)


class RegisterProviderHandler:
    def __init__(self, resolver: Resolver, transport: DirectTransport) -> None:
        self._resolver = resolver
        self._transport = transport

    def __call__(self, msg: RegisterProvider) -> Ok:
        self._resolver.register(
            msg.provider_id,
            msg.exports,
            scope=msg.caller_path or "/",
            visibility=msg.visibility,
        )
        if msg.service is not None:
            self._transport.register_provider(msg.provider_id, msg.service)
        return Ok()


class UnregisterProviderHandler:
    def __init__(self, resolver: Resolver, transport: DirectTransport) -> None:
        self._resolver = resolver
        self._transport = transport

    def __call__(self, msg: UnregisterProvider) -> Ok:
        self._resolver.unregister(msg.provider_id)
        self._transport.unregister_provider(msg.provider_id)
        return Ok()
