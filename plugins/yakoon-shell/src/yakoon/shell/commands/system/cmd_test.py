from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.models.command import CommandKind, CommandVisibility
from yakoon.base.runtime.session import Session


class CmdTest(Command):

    key = "test"
    template_prefix = "system"
    kind = CommandKind.BUILTIN
    visibility = CommandVisibility.DEVELOPER

    async def run(self, session: Session, request: Request) -> None:  # noqa: ARG002

        presenter = await self.get_presenter(session)
        ask1 = await presenter.prompts.ask("ask1")
        await session.emit(f" -> {ask1}")
        ask2 = await presenter.prompts.ask("ask2", policy="customer.age")
        await session.emit(f" -> {ask2}")
        ask3 = await presenter.prompts.ask_secret("ask3")
        await session.emit(f" -> {ask3}")
