import asyncio

from yakoon.base import ports
from yakoon.base.commands.command import CmdNotFound, Command, CommandContext
from yakoon.base.commands.request import Request
from yakoon.base.controllers.base import BaseController
from yakoon.base.directories.service import ServiceDirectory
from yakoon.base.models.input import DispatchInput
from yakoon.base.models.perm import Permission
from yakoon.base.models.workflow import WorkflowContextRequired
from yakoon.base.runtime.session import Session
from yakoon.platform.directories.controller import ControllerDirectory
from yakoon.platform.engines.command.router import CommandDirectory


class Engine:

    def __init__(
        self,
        directory: ControllerDirectory,
        services: ServiceDirectory,
        commands: CommandDirectory,
    ):
        self._directory = directory
        self._services = services
        self._commands = commands
        self._active_tasks: dict[str, asyncio.Task] = {}  # TODO: cleanup
        self._session_locks: dict[str, asyncio.Lock] = {}  # TODO: cleanup

    @property
    def services(self) -> ServiceDirectory:
        return self._services

    def _lock(self, session: Session) -> asyncio.Lock:
        skey = str(session.key)
        return self._session_locks.setdefault(skey, asyncio.Lock())

    async def _find_matching_command(
        self, active_router_id, request: Request
    ) -> tuple[BaseController, Command] | None:

        find = self._commands.find
        result: tuple[str, Command] = find(active_router_id, request.command)
        if result:
            active_router_id, command = result
            return self._directory.get(active_router_id), command

    async def dispatch(self, session: Session, di: DispatchInput) -> Session:

        skey = str(session.key)
        shell = self._directory.find_shell()
        if not session.get_active_controller():
            session.set_active_controller(shell.id)

        # 1) Prompt response path
        async with self._lock(session):
            dialog_service = self.services.get(ports.DialogService)
            if dialog_service.is_waiting(session):
                dialog_service.resolve_prompt(session, di.command)

                # Drive the existing active task until it either finishes or asks again
                await self._drive_until_blocked_or_done(session)

                # print("DISPATCH END")
                return session

        # 2) Normal command path
        loop = asyncio.get_running_loop()
        task = loop.create_task(self._dispatch_command(session, di))

        self._active_tasks[skey] = task

        await self._drive_until_blocked_or_done(session)
        return session

    async def _drive_until_blocked_or_done(self, session: Session) -> None:

        skey = str(session.key)
        task = self._active_tasks.get(skey)
        if not task:
            return

        dialogs = self.services.get(ports.DialogService)

        # drive until either:
        # - task done
        # - prompt state changes, then re-check
        while True:
            if task.done():
                _ = task.exception()  # drain
                self._active_tasks.pop(skey, None)
                return

            if dialogs.is_waiting(session):
                return

            # wait for either task completion OR a prompt edge
            edge = dialogs.edge_event(session)
            edge.clear()

            edge_task = asyncio.create_task(edge.wait())
            try:
                done, _ = await asyncio.wait(
                    {task, edge_task},
                    return_when=asyncio.FIRST_COMPLETED,
                )
            finally:
                edge_task.cancel()
                # don't await cancel; best-effort

    async def _dispatch_command(self, session: Session, di: DispatchInput) -> bool:
        failed = False
        request = Request(di.command)

        # Empty input -> noop (or fail, depending on your UX choice)
        if not request.command:
            return True

        # Active controller is the single routing context (S1)
        controller_id = session.get_active_controller()
        controller = self._directory.get(controller_id) if controller_id else None
        if not controller:
            await session.fail("Kein aktiver Controller gesetzt.")
            return False

        command = None

        try:
            # Domain-level hook before resolving the input into a command.
            # Allows dynamic command registration or early input rewriting.
            await controller.on_before_resolve(session)

            # Resolve command within the single active controller context (+ groups)
            result = await self._find_matching_command(controller_id, request)
            if not result:
                raise CmdNotFound(f"{request.command}")

            resolved_controller, command = result

            # check workflow context
            # user cannot start workflow commands without batch
            if command.requires_workflow and not di.batch_id:
                raise WorkflowContextRequired()

            # check permissions
            perm_service = self.services.get(ports.PermissionService)
            fq = Permission.fq_key(resolved_controller.id, command.key)
            if not perm_service.can_execute(session, fq):
                raise PermissionError("Permission denied")

            # Safety: Under S1, resolved controller should match active controller
            # (If your router can return a different controller, keep this;
            # otherwise you can drop it.)
            controller = resolved_controller
            command.context = CommandContext(controller, di.batch_id)

            # Pre-command hook
            await controller.on_before_run_command(session, request, command)

            # Execute command
            await command.run(session, request)

            # Post-command hook
            await controller.on_after_run_command(session, request, command)

        except WorkflowContextRequired:
            failed = True
            await session.fail(
                f"{request.command}': may only be executed from within a workflow.'"
            )

        except CmdNotFound as exc:
            failed = True
            await session.fail(f"{request.command}': command not found... use 'man'")
            self.wf_failed(exc, command, session, di)

        except PermissionError as exc:
            failed = True

            # command may be None if permission fails early
            audit = self._services.get(ports.AuditLogService)
            await audit.permission(
                session, "command", command.key if command else request.command
            )

            await session.fail(str(exc))
            self.wf_failed(exc, command, session, di)

        except ValueError as exc:
            failed = True
            await session.fail(str(exc))
            self.wf_failed(exc, command, session, di)

        except Exception as exc:
            failed = True
            audit = self._services.get(ports.AuditLogService)
            await audit.error(exc)
            await session.fail("Ein interner Fehler ist aufgetreten.")
            self.wf_failed(exc, command, session, di)

        finally:
            if command:
                command.context = None

            if failed and di.batch_id:
                wf = self._services.get(ports.WorkflowService)
                wf.cancel_batch(session, batch_id=di.batch_id)

            # Policy 2: cleanup the controller that executed this command
            # (NOT the current active controller after the command potentially
            # changed it)
            await controller.on_cleanup(session)

    def wf_failed(
        self, exc: Exception, command: Command, session: Session, di: DispatchInput
    ) -> bool:
        if di.batch_id:
            wf = self._services.get(ports.WorkflowService)
            wf.fail_batch(
                session,
                batch_id=di.batch_id,
                code=exc,
                message=str(exc),
                command=command.key,
            )
