"""Transport layer — IPC between SDK and Runtime Port Registry.

The transport is owned by the Executor, not by the Runtime.
Each executor kind creates its own transport:

  PythonExecutor  →  DirectTransport (in-process, synchronous)
  ProcessExecutor →  PipeTransport   (subprocess stdin/stdout)
  RemoteExecutor  →  SocketTransport (TCP/WebSocket)

The transport has exactly two operations:
  send(call) → Response    (used by the SDK)
  serve()                   (used by the Runtime to process calls)
"""

from __future__ import annotations

import json
from dataclasses import asdict

from .context import (
    Call,
    Response,
    _handle_wire,
)


class DirectTransport:
    """In-process transport. Synchronous call/response.

    Used by the PythonExecutor. Both send() and serve() operate
    in the same process — no actual IPC. The JSON serialization
    layer is preserved so the protocol boundary stays visible.
    """

    def send(self, call: Call) -> Response:
        wire = json.dumps(asdict(call))
        wire_result = _handle_wire(wire)
        data = json.loads(wire_result)
        return Response(result=data.get("result"), error=data.get("error"))

    def serve(self) -> None:
        """In-process: no listener needed — calls are processed synchronously."""
        return


_default_transport: DirectTransport | None = None


def get_transport() -> DirectTransport:
    global _default_transport
    if _default_transport is None:
        _default_transport = DirectTransport()
    return _default_transport


def set_transport(transport: DirectTransport) -> None:
    global _default_transport
    _default_transport = transport
