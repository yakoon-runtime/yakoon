"""Yakoon Standard Command — workspace Python.

Copyright 2024 Yakoon. Apache 2.0 license.
Demonstrates context and port access from a Python command.
"""

from y5n.sdk import context, ports


def main():
    """Demonstrates reading context and calling a port."""
    ctx = context.current()
    print(f"Path:    {ctx.path}")
    print(f"Args:    {(ctx.request or {}).get('args', [])}")
    print(f"Session: {(ctx.session or {}).get('key', '-')}")
    print()

    ports.provide("hello", {"greet": lambda name="World": f"Hello, {name}!"})
    hello = ports.get("hello")
    print(hello.greet())
    print(hello.greet(name="Yakoon"))


main()
