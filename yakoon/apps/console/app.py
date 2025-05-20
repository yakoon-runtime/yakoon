
import asyncio
from aioconsole import ainput
from yakoon.engine.runtime import Engine
from yakoon.game.definition import GameDefinition


async def error(exc: Exception):
    print(exc)


async def msg(text: str):
    print(text)


async def run_application(GameDef: GameDefinition):

    engine = Engine(GameDef)

    while True:
        command = await ainput("|:> ")
        async def on_ready(session):
            await engine.send(session, command)

        # each message is a own task.
        asyncio.create_task(
            engine.enter(None, msg, error, on_ready))


if __name__ == "__main__":
    asyncio.run(run_application(GameDefinition))
