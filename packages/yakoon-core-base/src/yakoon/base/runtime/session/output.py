
import inspect


def ensure_async(fn):
    if inspect.iscoroutinefunction(fn):
        return fn
    async def wrapped(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapped


class Output:
    """
    Adapter that encapsulates output and error handling for a session or interaction context.

    This class is used to decouple the engine and other logic from the concrete output mechanism
    (e.g., console print, WebSocket send, Telnet stream, test mock). It provides a consistent
    interface for writing messages and errors, and can optionally support buffering or flushing.

    Attributes:
        out (Callable[[str], Awaitable[None]]): Async function for standard output messages.
        err (Callable[[str], Awaitable[None]]): Async function for error or warning messages.
    """

    def __init__(self, out_fn=print, err_fn=print):
        self.out = ensure_async(out_fn)
        self.err = ensure_async(err_fn)

import json
import asyncio

class OutputWS:
    
    def __init__(self, ws, trace_id):
        self.ws = ws
        self.trace_id = trace_id
        self.out = ensure_async(self._make_sender("out"))
        self.err = ensure_async(self._make_sender("err"))

    def _make_sender(self, stream: str):
        async def send(text: str):
            payload = {
                "type": "loop_msg",
                "trace_id": self.trace_id,
                "stream": stream,
                "text": text
            }
            try:
                await self.ws.send(json.dumps(payload))
            except (ConnectionError, asyncio.CancelledError) as e:
                print(f"[WS][{stream}] Failed to send: {e}")
        return send
