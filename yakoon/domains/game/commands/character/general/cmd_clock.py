from yakoon.engine.core.command import Command
from yakoon.domains.game.services.season_service import get_season
from yakoon.domains.game.services.time_service import get_day_phase
from yakoon.engine.core.parser import Request
from yakoon.solution.platform.runtime.session import SolutionSession


class CmdClock(Command):

    key = "clock"
    
    async def run(self, session: SolutionSession, request: Request):
        controller = session.ctx.controller
        clock = controller.clock
        
        text = clock.get_formatted_time()        
        season = get_season(clock)
        phase = get_day_phase(clock)
        
        await session.emit(
            f"Aktuelle Spielzeit: {season.name}: {text} - Phase: {phase.name}")