from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session import Session


class CmdTest(Command):

    key = "test"    
    template_prefix = "system"

    async def run(self, session: Session, request: Request):
       
        presenter = await self.get_presenter(session)
        ask1 = await presenter.prompts.ask("ask1")
        await session.emit(ask1)
        ask2 = await presenter.prompts.ask("ask2")
        await session.emit(ask2)
        ask3 = await presenter.prompts.ask("ask3") 
        await session.emit(ask3)
