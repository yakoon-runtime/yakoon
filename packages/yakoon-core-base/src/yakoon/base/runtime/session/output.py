
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