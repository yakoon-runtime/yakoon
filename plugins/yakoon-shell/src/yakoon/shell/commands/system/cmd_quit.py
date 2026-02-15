from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session import Session


class CmdQuit(Command):

    key = "quit"
    template_prefix = "system"

    async def run(self, session: Session, request: Request) -> None:  # noqa: ARG002

        presenter = await self.get_presenter(session)
        ok = await presenter.prompts.ask("ask_really", policy="system:bool")
        if bool(ok):
            session.signal("exit_app")
