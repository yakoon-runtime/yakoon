
from yakoon.engine.core.command import Command
from yakoon.platform.render.context import Presenter


class RealmCommand(Command):

    def get_template_path(self) -> str:
        return f"domains/realm/commands/{self.template_key}"
    
    def get_presenter(self, session) -> Presenter:
        return Presenter(self.get_template_path(), session)