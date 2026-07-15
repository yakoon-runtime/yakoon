"""Resolver — transport-free mapping of port/method to provider.

The Resolver knows nothing about how a provider is reached.
It only knows which provider exports which capabilities,
and under which visibility policy they are available.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from .messages import Visibility


@dataclass
class _Route:
    provider_id: str
    scope: str  # path at registration time
    visibility: Visibility


class Resolver:
    """Maps port/method to provider_id, with visibility checks.

    Transport-free. CallHandler uses resolve() to find a provider,
    then the Transport delivers the call.
    """

    def __init__(self) -> None:
        self._providers: dict[str, dict[str, Sequence[str]]] = {}
        self._routes: dict[str, _Route] = {}  # "port:method" → Route

    def register(
        self,
        provider_id: str,
        exports: dict[str, Sequence[str]],
        *,
        scope: str = "/",
        visibility: Visibility = Visibility.GLOBAL,
    ) -> None:
        self._providers[provider_id] = exports
        for port, methods in exports.items():
            for method in methods:
                self._routes[f"{port}:{method}"] = _Route(
                    provider_id=provider_id,
                    scope=scope,
                    visibility=visibility,
                )

    def resolve(
        self,
        port: str,
        method: str,
        caller_path: str | None = None,
    ) -> str | None:
        route = self._routes.get(f"{port}:{method}")
        if route is None:
            return None

        caller_path = caller_path or "/"

        if route.visibility == Visibility.GLOBAL:
            return route.provider_id

        if route.visibility == Visibility.PARENT:
            if caller_path.startswith(route.scope) or caller_path == route.scope:
                return route.provider_id
            # auch vom Parent aus erreichbar
            if route.scope.startswith(caller_path):
                return route.provider_id
            return None

        if route.visibility == Visibility.LOCAL:
            if caller_path == route.scope:
                return route.provider_id
            return None

        return None

    def unregister(self, provider_id: str) -> None:
        exports = self._providers.pop(provider_id, {})
        for port, methods in exports.items():
            for method in methods:
                self._routes.pop(f"{port}:{method}", None)
