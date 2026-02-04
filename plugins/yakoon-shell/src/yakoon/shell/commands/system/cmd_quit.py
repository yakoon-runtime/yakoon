from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session import Session


class CmdQuit(Command):

    key = "quit"
    template_prefix = "system"

    async def run(self, session: Session, _: Request):

        presenter = await self.get_presenter(session)
        answer = await presenter.prompts.confirm("ask_really")
        if bool(answer):
            session.signal("exit_app")
