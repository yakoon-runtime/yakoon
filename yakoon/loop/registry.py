from typing import Callable

class CommandRegistry:
    _commands: dict[str, Callable] = {}

    @classmethod
    def register(cls, name: str, fn: Callable):
        cls._commands[name] = fn

    @classmethod
    def dispatch(cls, name: str, args: dict) -> dict:
        fn = cls._commands.get(name)
        if not fn:
            raise ValueError(f"Unknown command: {name}")
        return fn(args)
