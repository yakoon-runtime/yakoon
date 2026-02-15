from __future__ import annotations

from dataclasses import dataclass

from yakoon.base import ports
from yakoon.base.models.input import DispatchInput
from yakoon.base.ports import DialogState
from yakoon.base.runtime.session.session import Session
from yakoon.base.utils.format import format_ps1
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
        await self.engine.dispatch(self.session, DispatchInput(text))
        await self.drive()

    async def on_input_submit(self, values: dict[str, object]) -> None:
        dialogs = self.engine.services.get(ports.DialogService)
        dialogs.resolve_input(self.session, values)
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

            state = dialogs.state(self.session)
            ps1 = format_ps1(self.session)

            if state == DialogState.WAITING_FORM:
                spec = dialogs.get_form_spec(self.session)
                await self.host.on_input(ps1=ps1, spec=spec)
                return

            # Drain queued command handling
            di = queue.next_input(self.session)
            if di:
                await self.engine.dispatch(self.session, di)
                continue

            if hasattr(self.host, "on_ready"):
                await self.host.on_ready(ps1=ps1)
            else:
                await self.host.on_idle()
            return
