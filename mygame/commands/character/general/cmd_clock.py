from engine.core.command import Command
from mygame.services.season_service import get_season
from mygame.services.time_service import get_day_phase


class CmdClock(Command):
    key = "clock"
    
    async def run(self, session, request):
        clock = session.ctx.game.clock
        text = clock.get_formatted_time()
        
        season = get_season(clock)
        phase = get_day_phase(clock)
        
        await session.out(
            f"Aktuelle Spielzeit: {season.name}: {text} - Phase: {phase.name}")