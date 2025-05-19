from engine.core.command import Command
from mygame.services.time_service import get_day_phase

class CmdClock(Command):
    key = "clock"
    
    async def run(self, session, request):
        clock = session.ctx.game.clock
        text = clock.get_formatted_time()

        phase = get_day_phase(clock)
        await session.out(f"Aktuelle Spielzeit: {text} - Phase: {phase.name}")
