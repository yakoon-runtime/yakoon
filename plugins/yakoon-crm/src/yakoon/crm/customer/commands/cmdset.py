from typing import Sequence, Type
from yakoon.base.commands.command import Command
from yakoon.base.commands.commandset import CommandSet
from yakoon.workflow.commands.cmd_start import CmdWfStart

from yakoon.crm.customer.commands.cmd_create_customer import CmdCreateCustomer


class CrmCustomerCommands(CommandSet):
    
    group = "customer"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [
            CmdWfStart("create-customer"),
            CmdCreateCustomer,
            
        ]
