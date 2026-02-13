from dataclasses import dataclass

from yakoon.base import ports
from yakoon.base.models.input import DispatchInput
from yakoon.base.runtime.session.session import Session
from yakoon.base.utils.format import format_prompt

from yakoon.platform.engines.command.engine import Engine
from yakoon.platform.hosts.adapter import HostAdapter


@dataclass
class Runner:

    engine: Engine
    session: Session
    host: HostAdapter

    async def start(self, commands: list[str] | None = None) -> None:
        await self.drive(commands=commands)

    async def on_user_input(self, text: str) -> None:
        # Host liefert entweder normalen Command ODER Prompt-Antwort.
        await self.engine.dispatch(self.session, DispatchInput(text))
        await self.drive()

    async def on_cancel(self) -> None:
        await self.engine.dispatch(
            self.session, DispatchInput(command="shell:wf.cancel")
        )
        await self.drive()

    async def drive(self, *, commands: list[str] | None = None) -> None:
        dialogs = self.engine.services.get(ports.DialogService)
        queue = self.engine.services.get(ports.CommandQueueService)

        if commands:
            queue.enqueue_commands(self.session, commands)

        while True:
            if self.session.has_signal("exit_app"):
                await self.host.on_exit()
                return

            # If a prompt is waiting, we stop pumping and tell the host to collect input
            if dialogs.is_waiting(self.session):
                mode = dialogs.get_mode(self.session)
                prompt = format_prompt(self.session)
                await self.host.on_prompt(prompt=prompt, mode=mode)
                return

            # Otherwise drain queued commands
            di = queue.next_input(self.session)
            if di:
                await self.engine.dispatch(self.session, di)
                continue

            # optional: host may show a command prompt / enable input
            if hasattr(self.host, "on_ready"):
                prompt = format_prompt(self.session)
                await self.host.on_ready(prompt=prompt)
            else:
                await self.host.on_idle()
