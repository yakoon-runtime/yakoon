from yakoon.platform.commands.command import PlatformCommand


class CmdWelcome(PlatformCommand):

    key = "welcome"    
    requires = ["system"]

    async def run(self, session, request):
        await session.out("Yakoon sagt: 'Willkommen'.")