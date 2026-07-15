"""Resolver — transport-free mapping of port/method to provider.

The Resolver knows nothing about how a provider is reached.
It only knows which provider exports which capabilities.
"""

from __future__ import annotations

from collections.abc import Sequence


class Resolver:
    """Maps port/method to provider_id.

    Transport-free. CallHandler uses resolve() to find a provider,
    then the Transport delivers the call.
    """

    def __init__(self) -> None:
        self._providers: dict[str, dict[str, Sequence[str]]] = {}
        self._routes: dict[str, str] = {}  # "port:method" → provider_id

    def register(
        self,
        provider_id: str,
        exports: dict[str, Sequence[str]],
    ) -> None:
        self._providers[provider_id] = exports
        for port, methods in exports.items():
            for method in methods:
                self._routes[f"{port}:{method}"] = provider_id

    def resolve(self, port: str, method: str) -> str | None:
        return self._routes.get(f"{port}:{method}")

    def unregister(self, provider_id: str) -> None:
        exports = self._providers.pop(provider_id, {})
        for port, methods in exports.items():
            for method in methods:
                self._routes.pop(f"{port}:{method}", None)
