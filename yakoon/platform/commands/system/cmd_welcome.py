from yakoon.engine.core.command import Command


class CmdWelcome(Command):
    key = "welcome"
    
    async def run(self, session, request):
        await session.out("Yakoon sagt: 'Willkommen'.")