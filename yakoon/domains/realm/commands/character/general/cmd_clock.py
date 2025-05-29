from yakoon.domains.realm.commands.base import RealmCommand
from yakoon.domains.realm.services.season_service import get_season
from yakoon.domains.realm.services.time_service import get_day_phase
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
            season=get_season(clock),
            phase=get_day_phase(clock)
        )