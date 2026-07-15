from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass


@dataclass
class CommandContext:
    """Language-neutral command context.

    The runtime builds this from its internal objects and makes it
    available to the executor. The executor passes it to the command.
    The SDK wraps it into language-native objects.

    Fields are simple types (str, dict) so this can be serialized
    to JSON for non-Python executors.
    """

    path: str | None = None
    request: dict | None = None
    session: dict | None = None

    def __getitem__(self, key: str):
        return getattr(self, key)


_context_var: ContextVar[CommandContext] = ContextVar("y5n_command_context")

_port_registry: dict[str, dict] = {}
"""Global port registry. Lives in the runtime, not in any command.

Commands register services here via y5n.sdk.ports.register().
Services persist across command invocations within the same process.
"""


@dataclass
class Call:
    """A protocol-level invocation request.

    Language-neutral — can be serialized to JSON for non-Python transports.
    """

    port: str
    method: str
    args: dict | None = None


@dataclass
class Response:
    """A protocol-level invocation result.

    Language-neutral — can be serialized to JSON for non-Python transports.
    """

    result: object = None
    error: str | None = None


def invoke(call: Call) -> Response:
    """Execute a protocol-level Call against the port registry.

    This is the Runtime's invocation kernel. Every executor transport
    (direct call, socket, pipe, …) feeds into this function.
    """
    service = _port_registry.get(call.port)
    if service is None:
        return Response(error=f"port '{call.port}' not registered")

    fn = service.get(call.method)
    if fn is None:
        return Response(
            error=f"method '{call.method}' not found on port '{call.port}'"
        )

    args = call.args or {}
    try:
        result = fn(**args)
        return Response(result=result)
    except Exception as e:
        return Response(error=str(e))


def _set_context(ctx: CommandContext) -> None:
    _context_var.set(ctx)


class _Context:
    """Entry point for accessing the runtime context.

    Usage:
        ctx = context.current()
        print(ctx["request"])
    """

    @staticmethod
    def current() -> CommandContext:
        try:
            return _context_var.get()
        except LookupError:
            return CommandContext()


context = _Context()
