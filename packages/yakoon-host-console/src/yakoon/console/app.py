import asyncio

from yakoon.base import ports 
from yakoon.auth.controller import AuthCoreController
from yakoon.base.models.key import Key
from yakoon.base.models.input import DispatchInput
from yakoon.base.models.prompt import PromptMode
from yakoon.base.utils.format import format_prompt
from yakoon.base.utils.input import safe_input, safe_input_secret
from yakoon.base.runtime.devtools import MemoryTrendMonitor
from yakoon.base.runtime.devtools import UnresolvedPromptMonitor
from yakoon.crm.customer.controller import CrmCustomerCoreController
from yakoon.platform.directories.controller import ControllerDirectory

from yakoon.console.io import ConsoleOutput
from yakoon.compose.engine import compose_engine

from yakoon.base.models.format import OutputFormat
from yakoon.shell.controller import ShellCoreController
from yakoon.office.mailing.controller import OfficeMailingCoreController


command_inits = []
command_inits = ["use crm-customer", "create-customer"]

#command_inits += ["use auth", "su", "exit"]

async def run_console():
   
    session_key = Key.from_parts("yakoon", "bucket", "develop", "1",)
    
    engine = compose_engine(
        controllers=ControllerDirectory(
            controllers=[
                ShellCoreController(), 
                CrmCustomerCoreController(),
                AuthCoreController(),
                OfficeMailingCoreController()]))

    dialogs = engine.services.get(ports.DialogService)
    queue = engine.services.get(ports.CommandQueueService)
    sessions = engine.services.get(ports.SessionService)
    session, _ = await sessions.get_or_create(session_key)
    session.bind_io(ConsoleOutput())
    session.output_format = OutputFormat.MARKDOWN

    permissions = engine.services.get(ports.PermissionService)
    permissions.set_bootstrap_permissions(session)

    queue.enqueue_commands(session, command_inits)

    try:
        while True:
            prompt = format_prompt(session)
            try:
                di = None
                if dialogs.is_waiting(session):
                    mode = dialogs.get_mode(session)
                    if mode == PromptMode.SECRET:
                        di = DispatchInput(await safe_input_secret(prompt=prompt))
                    else:
                        di = DispatchInput(await safe_input(prompt=prompt))
                else:

                    di = queue.next_input(session)
                    if not di:
                        di = DispatchInput(await safe_input(prompt=prompt))

                await engine.dispatch(session, di)
                if session.has_signal("exit_app"):
                    break  

            except KeyboardInterrupt:
                if dialogs.is_waiting(session): # Ctrl+C wurde gedrückt
                    await engine.dispatch(session, DispatchInput(command="shell:wf.cancel"))
                    continue

    finally:
        sessions.release(session.key)


if __name__ == "__main__":    
   asyncio.run(run_console())
