from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from yakoon.base.controllers import BaseController
from yakoon.base.descriptors import TemplateSource
from yakoon.office.mailing.commands.cmdset import MailingCommands

if TYPE_CHECKING:
    from yakoon.base.commands.commandset import CommandSet


class OfficeMailingCoreController(BaseController):
    """Controller for the Office Mailing domain.

    Provides:
        - Mailing-related commands
        - Template root under yakoon.office.mailing:core
    """

    id: str = "office.mailing"

    template_source = TemplateSource(
        package="yakoon.office.mailing",
        template_sub_path="core",
    )

    @property
    def commandsets(self) -> Sequence[type[CommandSet]]:
        """Command sets exported by this controller."""
        return (MailingCommands,)
