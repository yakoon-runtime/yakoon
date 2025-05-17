import asyncio
from aioconsole import ainput

from engine.app import Engine
from mygame.game import GameDefinition

async def error(exc: Exception):
    print(exc)


async def msg(text: str):
    print(text)


async def run_console(engine):

    while True:
        command = await ainput("|:> ")
        async def on_session(session):
            await engine.listen(session, command)

        # each message is a own task.
        asyncio.create_task(
            engine.enter("1", msg, error, on_session))

if __name__ == "__main__":
    engine = Engine()
    engine.load_game(GameDefinition)
    asyncio.run(run_console(engine))
