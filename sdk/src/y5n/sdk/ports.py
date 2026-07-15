"""Port access — communicate with runtime services.

Usage:
    from y5n.sdk import ports

    ports.register("hello", {"greet": lambda name="World": f"Hello, {name}!"})

    hello = ports.get("hello")
    print(hello.greet(name="Yakoon"))
"""

from y5n.base.runtime.context import Call, _port_registry, invoke


class _PortProxy:
    """Proxy that turns attribute access into protocol-level calls.

    Internally sends a Call through the Runtime's invoke() function.
    The transport (direct call, socket, pipe, …) is pluggable below
    the invoke layer.
    """

    def __init__(self, port_name: str):
        self._port = port_name

    def __getattr__(self, name: str):
        def caller(**kwargs):
            response = invoke(
                Call(port=self._port, method=name, args=kwargs)
            )
            if response.error:
                raise RuntimeError(response.error)
            return response.result

        return caller


def register(name: str, service: dict) -> None:
    """Register a port service in the runtime."""
    _port_registry[name] = service


def get(name: str):
    """Get a port proxy by name."""
    if name not in _port_registry:
        raise KeyError(f"port '{name}' not registered")
    return _PortProxy(name)
