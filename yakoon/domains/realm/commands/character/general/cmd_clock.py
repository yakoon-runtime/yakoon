from yakoon.domains.realm.commands.base import RealmCommand
from yakoon.domains.realm.services.day_phase import DayPhaseService
from yakoon.domains.realm.services.season import SeasonService
from yakoon.commands.parser import Request
from yakoon.runtime.models.session import BaseSession


class CmdClock(RealmCommand):

    key = "clock"
    template_key = "character/general/cmd_clock"
    
    async def run(self, session: BaseSession, request: Request):
        presenter = await self.get_presenter(session)

        clock = self.controller.clock

        await presenter.emit("show",
            time=clock.get_formatted_time(),
            season=SeasonService.get_season_by_clock(clock),
            phase=DayPhaseService.get_day_phase_by_clock(clock)
        )