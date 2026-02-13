from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from uuid import uuid4

from yakoon.base import ports
from yakoon.base.models.workflow import WorkflowError, WorkflowRuntime, WorkflowStatus
from yakoon.workflow.runtime.compiler import compile_run_command


class WorkflowNotFound(KeyError):
    pass


class WorkflowService:
    """
    Keine Caches hier: jedes get_def() lädt on-demand über ControllerCatalog +
    WorkflowLoaderService.

    Regeln:
    - Workflows sind controller-scoped (controller_id + workflow_key).
    - interaction_mode kommt IMMER aus der Session.
    - Commands müssen keine split_id/normalize machen
    (Engine/Router verhindert Cross-Controller).
    """

    def __init__(self, services):
        self.services = services

    # ---- runtime access ----

    def runtime(self, session) -> WorkflowRuntime:
        meta = session._runtime.meta
        rt = meta.get("workflow")
        if rt is None:
            rt = WorkflowRuntime()
            meta["workflow"] = rt
        return rt

    # ---- loading (no caching) ----

    def get_def(self, controller_id: str, workflow_key: str):
        catalog = self.services.get(ports.ControllerCatalogService)
        info = catalog.get(controller_id)
        if not info or not info.workflow_source:
            raise WorkflowNotFound(
                f"Workflow not found: {controller_id}:{workflow_key}"
            )

        loader = self.services.get(ports.WorkflowCompileService)
        wf = loader.load_def(info.workflow_source, workflow_key)
        if not wf:
            raise WorkflowNotFound(
                f"Workflow not found: {controller_id}:{workflow_key}"
            )

        return wf

    # ---- orchestration (v1: prompt/run/end, linear next) ----

    def set_value(self, session, batch_id: str, key: str, value: Any) -> None:
        rt = self.runtime(session)
        batch = rt.get(batch_id)
        if not batch:
            raise RuntimeError(f"Unknown workflow batch: {batch_id}")
        batch.values[key] = value

    def start_with_values(
        self,
        session,
        controller_id: str,
        workflow_key: str,
        values: Mapping[str, Any],
        *,
        enqueue_first: bool = True,
        ignore_none: bool = True,
    ) -> str:
        """
        Convenience wrapper:
        - creates workflow batch
        - sets initial batch.values
        - enqueues first step (default)

        Args:
            enqueue_first:
                If True, enqueue the first step AFTER values were set.
                If False, caller may enqueue manually (rare).
            ignore_none:
                If True, keys with value None are not written into batch.values.
                This keeps 'missing' semantics intact.
        """
        batch_id = self.start(
            session,
            controller_id=controller_id,
            workflow_key=workflow_key,
            enqueue_first=False,
        )

        for k, v in values.items():
            if ignore_none and v is None:
                continue
            self.set_value(session, batch_id, k, v)

        if enqueue_first:
            self.enqueue_next(session, batch_id)

        return batch_id

    def start(
        self,
        session,
        controller_id: str,
        workflow_key: str,
        *,
        enqueue_first: bool = True,
    ) -> str:
        wf = self.get_def(controller_id, workflow_key)

        batch_id = uuid4().hex

        rt = self.runtime(session)
        batch = rt.ensure(batch_id, interaction_mode=session.interaction_mode)
        batch.controller_id = controller_id
        batch.workflow_key = workflow_key
        batch.current_step = wf.start
        batch.pending_step = None
        batch.status = (
            WorkflowStatus.RUNNING if enqueue_first else WorkflowStatus.PREPARED
        )
        if enqueue_first:
            self.enqueue_next(session, batch_id)

        return batch_id

    def resume_with_values(
        self,
        session,
        batch_id: str,
        values: Mapping[str, Any],
        *,
        ignore_none: bool = True,
        enqueue_next: bool = True,
    ) -> None:
        """
        Convenience:
        - set/override multiple values in an existing workflow batch
        - then continue workflow by enqueuing the next step (default)

        Typical use:
        - GUI form submits multiple fields at once
        - a command collects several values and wants to continue

        wf.resume_with_values(session, batch_id, {
            "customer.first_name": first,
            "customer.last_name": last,
            "customer.email": email,
        })
        """
        rt = self.runtime(session)
        batch = rt.get(batch_id)
        if not batch:
            raise RuntimeError(f"Unknown workflow batch: {batch_id}")

        for k, v in values.items():
            if ignore_none and v is None:
                continue
            self.set_value(session, batch_id, k, v)

        if enqueue_next:
            self.enqueue_next(session, batch_id)

    def get_step(self, session, batch_id: str, step_id: str):
        rt = self.runtime(session)
        batch = rt.get(batch_id)
        if not batch or not batch.controller_id or not batch.workflow_key:
            raise RuntimeError(f"Unknown workflow batch: {batch_id}")

        wf = self.get_def(batch.controller_id, batch.workflow_key)
        step = wf.steps.get(step_id)
        if not step:
            raise KeyError(
                f"Step not found: {batch.controller_id}:{batch.workflow_key}::{step_id}"
            )
        return step

    def enqueue_next(self, session, batch_id: str) -> None:
        """
        Enqueued exakt 1 'next thing':
          - prompt-step => wf.prompt <batch_id> <step_id>
          - run-step    => <real_command>; wf.next <batch_id> <step_id>
          - end-step    => cleanup
        """
        rt = self.runtime(session)
        batch = rt.get(batch_id)
        if not batch or not batch.controller_id or not batch.workflow_key:
            return

        if batch.status == WorkflowStatus.PREPARED:
            batch.status = WorkflowStatus.RUNNING

        wf = self.get_def(batch.controller_id, batch.workflow_key)
        step_id = batch.current_step or wf.start
        step = wf.steps.get(step_id)
        if not step:
            raise KeyError(
                f"Step not found: {batch.controller_id}:{batch.workflow_key}::{step_id}"
            )

        queue = self.services.get(ports.CommandQueueService)

        # END
        if step.end:
            batch.status = WorkflowStatus.DONE
            rt.remove(batch_id)
            return

        # PROMPT
        if step.prompt:
            queue.enqueue_commands(
                session, [f"wf.prompt {batch_id} {step.id}"], batch_id=batch_id
            )
            batch.pending_step = step.id
            return

        # SWITCH
        if step.switch:
            rendered = compile_run_command(
                step.switch.expr,
                batch.values,
                context=f"{batch.controller_id}:{batch.workflow_key}:{step.id}",
            ).strip()

            key = rendered.strip().lower()
            next_id = step.switch.cases.get(key)

            if not next_id:
                if step.switch.default:
                    next_id = step.switch.default
                else:
                    raise RuntimeError(
                        f"Switch step '{step.id}': no case for '{key}' and no default"
                    )

            batch.current_step = next_id
            self.enqueue_next(session, batch_id)
            return

        # RUN
        if step.run:
            cmd = compile_run_command(
                step.run,
                batch.values,
                context=f"{batch.controller_id}:{batch.workflow_key}:{step.id}",
            )
            queue.enqueue_commands(
                session, [cmd, f"wf.next {batch_id} {step.id}"], batch_id=batch_id
            )
            return

        raise ValueError(f"Invalid step '{step.id}': neither prompt nor run nor end")

    def complete_prompt_step(
        self, session, *, batch_id: str, step_id: str, value: Any
    ) -> None:
        rt = self.runtime(session)
        batch = rt.get(batch_id)
        if not batch:
            return

        step = self.get_step(session, batch_id, step_id)
        if not step.prompt or not step.prompt.var:
            raise RuntimeError(f"Step {step_id} is not a prompt with 'var'")

        batch.values[step.prompt.var] = value
        batch.pending_step = None

        if step.branch:
            key = str(value).lower()
            next_id = step.branch.get(key)
            if not next_id:
                raise RuntimeError(
                    f"Prompt step '{step.id}': branch has no target for '{key}'"
                )
            batch.current_step = next_id
            self.enqueue_next(session, batch_id)
            return

        if not step.next:
            raise RuntimeError(f"Prompt step '{step.id}' has no 'next'")

        batch.current_step = step.next
        self.enqueue_next(session, batch_id)

    def complete_run_step(self, session, *, batch_id: str, step_id: str) -> None:
        rt = self.runtime(session)
        batch = rt.get(batch_id)
        if not batch:
            return

        step = self.get_step(session, batch_id, step_id)
        if not step.run:
            raise RuntimeError(f"Step {step_id} is not a run step")

        if not step.next:
            rt.remove(batch_id)
            return

        batch.current_step = step.next
        self.enqueue_next(session, batch_id)

    def fail_batch(
        self,
        session,
        *,
        batch_id: str,
        code: str,
        message: str,
        command: str | None = None,
    ) -> None:

        rt = self.runtime(session)
        batch = rt.get(batch_id)
        if not batch:
            return

        step_id = batch.pending_step or batch.current_step
        batch.status = WorkflowStatus.FAILED
        batch.error = WorkflowError(
            code=code, message=message, step_id=step_id, command=command
        )

    def cancel_batch(self, session, *, batch_id: str) -> None:

        rt = self.runtime(session)
        batch = rt.get(batch_id)
        if not batch:
            return

        batch.status = WorkflowStatus.CANCELLED
        batch.error = None

        queue = self.services.get(ports.CommandQueueService)
        queue.cancel_batch(session, batch_id)
