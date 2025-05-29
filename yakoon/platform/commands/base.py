
from yakoon.engine.core.command import Command
from yakoon.platform.render.context import Presenter


class PlatformCommand(Command):

    def get_template_path(self) -> str:
        return f"platform/commands/{self.template_key}"
    
    def get_presenter(self, session) -> Presenter:
        return Presenter(self.get_template_path(), session)