from yakoon.domains.realm.commands.base import RealmCommand
from yakoon.domains.realm.services.day_phase import DayPhaseService
from yakoon.domains.realm.services.season import SeasonService
from yakoon.engine.core.parser import Request
from yakoon.solution.platform.runtime.session import SolutionSession


class CmdClock(RealmCommand):

    key = "clock"
    template_key = "character/general/cmd_clock"
    
    async def run(self, session: SolutionSession, request: Request):
        presenter = self.get_presenter(session)

        controller = session.ctx.controller
        clock = controller.clock

        await presenter.emit("show",
            time=clock.get_formatted_time(),
            season=SeasonService.get_season_by_clock(clock),
            phase=DayPhaseService.get_day_phase_by_clock(clock)
        )