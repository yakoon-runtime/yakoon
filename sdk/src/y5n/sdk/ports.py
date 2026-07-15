"""Port access — communicate with runtime services.

Usage:
    from y5n.sdk import ports

    ports.register("hello", {"greet": lambda name="World": f"Hello, {name}!"})

    hello = ports.get("hello")
    print(hello.greet(name="Yakoon"))
"""

import uuid

from y5n.base.runtime.bus import get_bus
from y5n.base.runtime.context import Call, invoke
from y5n.base.runtime.messages import RegisterProvider


class _PortProxy:
    def __init__(self, port_name: str):
        self._port = port_name

    def __getattr__(self, name: str):
        def caller(**kwargs):
            response = invoke(Call(port=self._port, method=name, args=kwargs))
            if response.error:
                raise RuntimeError(response.error)
            return response.result

        return caller


def register(name: str, service: dict) -> None:
    """Register a port service in the runtime."""
    provider_id = f"provider:{uuid.uuid4().hex}"
    get_bus().dispatch(
        RegisterProvider(
            provider_id=provider_id,
            exports={name: list(service.keys())},
            service=service,
        )
    )


def get(name: str):
    """Get a port proxy by name.

    Note: this does not verify the port exists — the Resolver
    will reject calls to unknown ports at invoke time.
    """
    return _PortProxy(name)
