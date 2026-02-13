from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from yakoon.base.controllers import BaseController
from yakoon.base.descriptors import TemplateSource
from yakoon.base.descriptors.workflow import WorkflowSource
from yakoon.crm.customer.commands.cmdset import CrmCustomerCommands

if TYPE_CHECKING:
    from yakoon.base.commands.commandset import CommandSet


class CrmCustomerCoreController(BaseController):
    """Controller for CRM customer management.

    Provides:
        - Customer-related commands
        - Customer workflows
        - Templates and workflows under yakoon.crm.customer:customer
    """

    id: str = "crm-customer"

    template_source = TemplateSource(
        package="yakoon.crm.customer",
        template_sub_path="customer",
    )

    workflow_source = WorkflowSource(
        package="yakoon.crm.customer",
        workflow_sub_path="customer",
    )

    @property
    def commandsets(self) -> Sequence[type[CommandSet]]:
        """Command sets exported by this controller."""
        return (CrmCustomerCommands,)
