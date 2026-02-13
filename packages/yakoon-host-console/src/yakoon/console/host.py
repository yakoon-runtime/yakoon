import asyncio
from yakoon.base.models.prompt import PromptMode
from yakoon.base.utils.input import safe_input, safe_input_secret
from yakoon.platform.hosts.adapter import HostAdapter


class ConsoleHost(HostAdapter):
    """
    Console UI adapter. It does NOT run the engine. It only:
    - asks for user input when requested
    - forwards the input via the provided submit callback
    """

    def __init__(self, submit):

        self._submit = submit
        self._lock = asyncio.Lock()

    async def on_prompt(self, *, prompt: str, mode: PromptMode) -> None:
        # Prevent parallel prompts (important in async environments)
        async with self._lock:
            if mode == PromptMode.SECRET:
                text = await safe_input_secret(prompt=prompt)
            else:
                text = await safe_input(prompt=prompt)
        await self._submit(text)

    async def on_ready(self, *, prompt: str) -> None:
        # In console: "ready" means we can read a normal command line.
        async with self._lock:
            text = await safe_input(prompt=prompt)
        if text.strip():
            await self._submit(text)

    async def on_idle(self) -> None:
        # Optional: idle same as ready, or do nothing.
        return

    async def on_exit(self) -> None:
        return
