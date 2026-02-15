import asyncio

from yakoon.base.models.fields import FormSpec
from yakoon.base.utils.input import safe_input, safe_input_secret
from yakoon.platform.hosts.adapter import HostAdapter


class ConsoleHost(HostAdapter):
    """
    Console UI adapter.

    It does NOT run the engine.
    It only:
    - renders field/form requests
    - collects user input
    - forwards input via the provided submit callback
    """

    def __init__(self, submit):
        self._submit = submit
        self._lock = asyncio.Lock()

    async def on_input(self, *, ps1: str, spec: FormSpec) -> None:

        values: dict[str, object] = {}

        for field in spec.fields:
            prompt = field.label or field.key
            if field.hint:
                prompt = f"{prompt} ({field.hint})"
            prompt = f"{ps1}[{prompt}]"

            async with self._lock:
                if getattr(field, "secret", False):
                    value = await safe_input_secret(ps1=prompt)
                else:
                    value = await safe_input(ps1=prompt)

            values[field.key] = value

        # For console, we submit the whole form as a dict.
        await self._submit(values)

    async def on_ready(self, *, ps1: str) -> None:
        async with self._lock:
            text = await safe_input(ps1=ps1)

        if text.strip():
            await self._submit(text)

    async def on_idle(self) -> None:
        return

    async def on_exit(self) -> None:
        return
