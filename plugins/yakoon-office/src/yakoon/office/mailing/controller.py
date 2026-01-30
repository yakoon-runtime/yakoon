
from yakoon.base.controllers import BaseController
from yakoon.base.descriptors import TemplateSource
from yakoon.base.runtime.session.session import Session
from yakoon.office.mailing.commands.cmdset import MailingCommands


class OfficeMailingController(BaseController):

    id = "office.mailing"
    
    template_source = TemplateSource(
        name="yakoon.office",
        package="yakoon.office.mailing",
        package_path="templates"
    )

    commandsets = [
        MailingCommands]
        
    async def on_initialize(self, session: Session):
        session.cmd_groups_dynamic = ["office.mailing:system"]



