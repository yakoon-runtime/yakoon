import asyncio

from yakoon.auth.controller import AuthCoreController
from yakoon.base import ports
from yakoon.base.models.format import OutputFormat
from yakoon.base.models.key import Key
from yakoon.compose.engine import compose_engine
from yakoon.console.host import ConsoleHost
from yakoon.console.io import ConsoleOutput
from yakoon.crm.customer.controller import CrmCustomerCoreController
from yakoon.office.mailing.controller import OfficeMailingCoreController
from yakoon.platform.directories.controller import ControllerDirectory
from yakoon.platform.hosts.runner import Runner
from yakoon.shell.controller import ShellCoreController


async def run_console():

    engine = compose_engine(
        controllers=ControllerDirectory(
            controllers=[
                ShellCoreController(),
                CrmCustomerCoreController(),
                AuthCoreController(),
                OfficeMailingCoreController(),
            ]
        )
    )

    sessions = engine.services.get(ports.SessionService)
    session, _ = await sessions.get_or_create(
        Key.from_parts(
            "yakoon",
            "bucket",
            "develop",
            "1",
        )
    )

    session.bind_io(ConsoleOutput())
    session.output_format = OutputFormat.MARKDOWN
    # session.interaction_mode = InteractionMode.FORM

    permissions = engine.services.get(ports.PermissionService)
    permissions.set_bootstrap_permissions(session)

    try:

        async def submit(text: str):
            await runner.on_user_input(text)

        host = ConsoleHost(submit=submit)
        runner = Runner(engine=engine, session=session, host=host)

        inits = ["use crm-customer", "customer-create"]
        # inits = []
        await runner.start(inits)

    except KeyboardInterrupt:
        # Ctrl+C: if a prompt is active, cancel it; otherwise ignore or exit
        dialogs = engine.services.get(ports.DialogService)
        if dialogs.is_waiting(session):
            await runner.on_cancel()
    finally:
        sessions.release(session.key)


if __name__ == "__main__":
    asyncio.run(run_console())
