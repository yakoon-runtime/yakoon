from yakoon.domains.game.runtime.data import RuntimeGameData
from yakoon.engine.core.command import Command
from yakoon.engine.core.parser import Request
from yakoon.solution.platform.runtime.session import SolutionSession


class CmdOOC(Command):

    key = "ooc"
    requires_character = True

    async def run(self, session: SolutionSession, request: Request):
        runtime_data: RuntimeGameData = session.data_runtime
        if not runtime_data.character:
            return await session.err("Du bist bereits OOC.")
        
        name = runtime_data.character.name
        session.data_storage.rem(session.ctx.controller.name, "char_id")
        await session.send_msg(f"Du bist nun OOC. Charakter '{name}' wurde verlassen.")