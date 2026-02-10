
from yakoon.base.controllers import BaseController
from yakoon.base.descriptors import TemplateSource
from yakoon.base.descriptors.workflow import WorkflowSource
from yakoon.crm.customer.commands.cmdset import CrmCustomerCommands


class CrmCustomerCoreController(BaseController):

    id = "crm-customer"
    
    template_source = TemplateSource(
        package="yakoon.crm.customer"
        )

    workflow_source = WorkflowSource(
        package="yakoon.crm.customer"
        )

    commandsets = [
        CrmCustomerCommands]
        