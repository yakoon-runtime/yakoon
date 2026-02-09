
from yakoon.base.controllers.base import BaseController
from yakoon.base.models.key import Key
from yakoon.base.models.ns import Namespace
from yakoon.base.ports import SessionService
from yakoon.base.descriptors.template import TemplateSource
from yakoon.base.runtime.session import Session

from yakoon.auth.commands.cmdset import AuthSystemCommands


class AuthCoreController(BaseController):

    id: str = "auth"

    is_shell: bool = False
    is_listed: bool = True
    is_activatable: bool = True

    template_source = TemplateSource(
        package="yakoon.auth",
        template_sub_path="core")

    commandsets = [
        AuthSystemCommands]
