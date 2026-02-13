from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from yakoon.auth.commands.cmdset import AuthSystemCommands
from yakoon.base.controllers.base import BaseController
from yakoon.base.descriptors.template import TemplateSource

if TYPE_CHECKING:
    from yakoon.base.commands.commandset import CommandSet


class AuthCoreController(BaseController):
    """Authentication controller.

    Provides:
        - System-level authentication commands
        - Templates under yakoon.auth:core
    """

    id: str = "auth"

    is_shell: bool = False
    is_listed: bool = True
    is_activatable: bool = True

    template_source = TemplateSource(
        package="yakoon.auth",
        template_sub_path="core",
    )

    @property
    def commandsets(self) -> Sequence[type[CommandSet]]:
        """Command sets exported by this controller."""
        return (AuthSystemCommands,)
