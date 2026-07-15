from __future__ import annotations

import json
from contextvars import ContextVar
from dataclasses import asdict, dataclass


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

    Serializes Call to the wire format and delegates to _handle_wire().
    Every executor transport (direct, socket, pipe, …) follows this
    same pattern: serialize → transport → deserialize.

    The transport below this function does NOT know it is Python — it
    exchanges JSON strings as if speaking to a foreign process.
    """
    wire = json.dumps(asdict(call))
    wire_result = _handle_wire(wire)
    data = json.loads(wire_result)
    return Response(result=data.get("result"), error=data.get("error"))


def _handle_wire(wire: str) -> str:
    """Process a wire-format invocation and return a wire-format result.

    This is the "server side" of the protocol. In a subprocess executor
    it would run in the parent process over a pipe. Here it runs inline.
    """
    data = json.loads(wire)
    service = _port_registry.get(data.get("port"))
    if service is None:
        return json.dumps({"error": f"port '{data.get('port')}' not registered"})

    fn = service.get(data.get("method"))
    if fn is None:
        return json.dumps(
            {"error": f"method '{data.get('method')}' not found on port '{data.get('port')}'"}
        )

    args = data.get("args") or {}
    try:
        result = fn(**args)
        return json.dumps({"result": result})
    except Exception as e:
        return json.dumps({"error": str(e)})


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
