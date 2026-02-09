
from yakoon.base.controllers import BaseController
from yakoon.base.descriptors import TemplateSource
from yakoon.base.runtime.session.session import Session
from yakoon.office.mailing.commands.cmdset import MailingCommands


class OfficeMailingCoreController(BaseController):

    id = "office.mailing"
    
    template_source = TemplateSource(
        package="yakoon.office.mailing",
        template_sub_path="core")

    commandsets = [
        MailingCommands]
        