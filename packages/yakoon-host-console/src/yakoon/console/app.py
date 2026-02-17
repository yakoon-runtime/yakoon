import asyncio

from yakoon.auth.controller import AuthCoreController
from yakoon.base import ports
from yakoon.base.models.key import Key
from yakoon.compose.engine import compose_engine
from yakoon.console.host import ConsoleHost
from yakoon.console.io import ConsoleOutput
from yakoon.crm.customer.controller import CrmCustomerCoreController
from yakoon.office.mailing.controller import OfficeMailingCoreController
from yakoon.platform.directories.controller import ControllerDirectory
from yakoon.platform.hosts.runner import Runner
from yakoon.shell.controller import ShellCoreController


async def run_console() -> None:
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
        Key.from_parts("yakoon", "bucket", "develop", "1")
    )

    # All visible output is rendered via session IO.
    session.bind_io(ConsoleOutput())

    permissions = engine.services.get(ports.PermissionService)
    permissions.set_bootstrap_permissions(session)

    runner: Runner | None = None

    async def submit(payload) -> None:

        if isinstance(payload, dict):
            await runner.on_input_submit(payload)
            return

        await runner.on_user_input(str(payload))

    try:
        host = ConsoleHost(submit=submit)
        runner = Runner(engine=engine, session=session, host=host)

        inits: list[str] = []
        await runner.start(inits)

    except KeyboardInterrupt:
        dialogs = engine.services.get(ports.DialogService)
        if dialogs.is_waiting(session):
            await runner.on_cancel()  # type: ignore[union-attr]
    finally:
        sessions.release(session.key)


if __name__ == "__main__":
    asyncio.run(run_console())
