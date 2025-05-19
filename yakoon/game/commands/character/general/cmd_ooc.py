from yakoon.engine.core.command import Command
from yakoon.engine.core.parser import Request
from yakoon.game.runtime.session import GameSession


class CmdOOC(Command):

    key = "ooc"

    async def run(self, session: GameSession, request: Request):
        if not session.character:
            return await session.err("Du bist bereits OOC.")

        name = session.character.name
        session.character = None
        session.command_groups = ["account"]
        await session.out(f"Du bist nun OOC. Charakter '{name}' wurde verlassen.")