from collections.abc import Sequence

from yakoon.base.commands.command import Command
from yakoon.base.commands.commandset import CommandSet
from yakoon.crm.customer.commands.cmd_customer_store import CmdCustomerStore
from yakoon.crm.customer.commands.cmd_customer_validate import CmdCustomerValidate
from yakoon.workflow.commands.cmd_start import CmdWfStart


class CrmCustomerCommands(CommandSet):

    group = "customer"

    @classmethod
    def commands(cls) -> Sequence[type[Command]]:
        return [
            CmdWfStart("customer-create"),
            CmdCustomerStore,
            CmdCustomerValidate,
        ]
