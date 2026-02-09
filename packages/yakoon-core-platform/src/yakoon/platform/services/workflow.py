from __future__ import annotations

import re
import json
import yaml
import importlib.resources as ir

from typing import Any, Dict
from yakoon.base import ports
from yakoon.base.descriptors.workflow import WorkflowSource
from yakoon.base.models.workflow import PromptDef, StepDef, WorkflowDef, WorkflowRuntime


class WorkflowNotFound(KeyError):
    pass


_ARG_PATTERN = re.compile(r"""
    (?P<flag>--\w+)\s+
    (?P<placeholder>\{\{[^}]+\}\})
""", re.VERBOSE)


class WorkflowService:
    """
    Keine Caches hier: jedes get_def() lädt on-demand über ControllerCatalog + WorkflowLoaderService.

    Regeln:
    - Workflows sind controller-scoped (controller_id + workflow_key).
    - interaction_mode kommt IMMER aus der Session.
    - Commands müssen keine split_id/normalize machen (Engine/Router verhindert Cross-Controller).
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
            raise WorkflowNotFound(f"Workflow not found: {controller_id}:{workflow_key}")

        loader = self.services.get(ports.WorkflowCompileService)
        wf = loader.load_def(info.workflow_source, workflow_key)
        if not wf:
            raise WorkflowNotFound(f"Workflow not found: {controller_id}:{workflow_key}")

        return wf

    # ---- orchestration (v1: prompt/run/end, linear next) ----

    def start(self, session, controller_id: str, workflow_key: str) -> str:
        """
        Startet einen Run als neue batch_id und queued NUR den ersten Step.
        interaction_mode kommt ausschließlich aus session.interaction_mode.
        """
        wf = self.get_def(controller_id, workflow_key)

        queue = self.services.get(ports.CommandQueueService)
        batch_id = queue.enqueue_commands(session, [], batch_id=None)

        rt = self.runtime(session)
        batch = rt.ensure(batch_id, interaction_mode=session.interaction_mode)
        batch.controller_id = controller_id
        batch.workflow_key = workflow_key
        batch.current_step = wf.start
        batch.pending_step = None

        self.enqueue_next(session, batch_id)
        return batch_id

    def get_step(self, session, batch_id: str, step_id: str):
        rt = self.runtime(session)
        batch = rt.get(batch_id)
        if not batch or not batch.controller_id or not batch.workflow_key:
            raise RuntimeError(f"Unknown workflow batch: {batch_id}")

        wf = self.get_def(batch.controller_id, batch.workflow_key)
        step = wf.steps.get(step_id)
        if not step:
            raise KeyError(f"Step not found: {batch.controller_id}:{batch.workflow_key}::{step_id}")
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

        wf = self.get_def(batch.controller_id, batch.workflow_key)
        step_id = batch.current_step or wf.start
        step = wf.steps.get(step_id)
        if not step:
            raise KeyError(f"Step not found: {batch.controller_id}:{batch.workflow_key}::{step_id}")

        queue = self.services.get(ports.CommandQueueService)

        # END
        if step.end:
            rt.remove(batch_id)
            return

        # PROMPT
        if step.prompt:
            queue.enqueue_commands(
                session, [f"wf.prompt {batch_id} {step.id}"], batch_id=batch_id)
            batch.pending_step = step.id
            return

        # RUN
        if step.run:
            cmd = self._render_run(step.run, batch.values)
            queue.enqueue_commands(
                session, [cmd, f"wf.next {batch_id} {step.id}"], batch_id=batch_id)
            return

        raise ValueError(f"Invalid step '{step.id}': neither prompt nor run nor end")

    def apply_prompt_value(self, session, *, batch_id: str, step_id: str, value: Any) -> None:
        rt = self.runtime(session)
        batch = rt.get(batch_id)
        if not batch:
            return

        step = self.get_step(session, batch_id, step_id)
        if not step.prompt or not step.prompt.var:
            raise RuntimeError(f"Step {step_id} is not a prompt with 'var'")

        batch.values[step.prompt.var] = value
        batch.pending_step = None

        if not step.next:
            raise RuntimeError(f"Prompt step '{step.id}' has no 'next'")

        batch.current_step = step.next
        self.enqueue_next(session, batch_id)

    def advance_after_run(self, session, *, batch_id: str, step_id: str) -> None:
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

    def set_value(self, session, batch_id: str, key: str, value: Any) -> None:
        rt = self.runtime(session)
        batch = rt.get(batch_id)
        if not batch:
            raise RuntimeError(f"Unknown workflow batch: {batch_id}")
        batch.values[key] = value

    # ---- tiny templating (v1) ----

    @staticmethod
    def _render_run(cmd: str, values: dict[str, Any]) -> str:
        out = cmd

        # 1) Named arguments behandeln: --flag {{key}}
        def replace_named(match):
            flag = match.group("flag")
            placeholder = match.group("placeholder")
            key = placeholder[2:-2].strip()  # {{user.name}} -> user.name
            val = values.get(key)

            if val is None or val == "":
                return ""  # komplettes Argument entfernen

            return f"{flag} {val}"

        out = _ARG_PATTERN.sub(replace_named, out)

        # 2) übrige {{key}} ersetzen (positional fallback)
        for k, v in values.items():
            placeholder = "{{" + k + "}}"
            if v is None or v == "":
                out = out.replace(placeholder, "")
            else:
                out = out.replace(placeholder, str(v))

        # 3) whitespace normalisieren
        out = " ".join(out.split())
        return out


class WorkflowFileNotFound(FileNotFoundError):
    pass


class WorkflowCompileService:
    """
    Loads exactly ONE workflow definition from package resources.

    Rules:
    - 1 workflow == 1 file
    - filename == <workflow_key>.(yaml|yml|json)
    - no caching, no bulk loading
    """

    # ----------------------------
    # public API
    # ----------------------------

    def load_def(self, source: WorkflowSource, workflow_key: str) -> WorkflowDef:
        """
        Load and parse a single workflow file.

        Args:
            source: WorkflowSource describing the package/path
            workflow_key: file stem (without extension)

        Returns:
            Parsed workflow data (dict)

        Raises:
            WorkflowNotFound if file does not exist
            ValueError for invalid content
        """
        root = ir.files(source.package) / source.workflow_path / source.workflow_sub_path
        if not root.is_dir():
            raise WorkflowNotFound(f"Workflow directory not found: {root}")

        path = self._find_file(root, workflow_key)
        raw_text = path.read_text(encoding="utf-8")
        raw = self._parse(path.name, raw_text)

        return self._build_workflow_def(workflow_key, raw)

    def _find_file(self, root, workflow_key: str):
        for ext in (".yaml", ".yml", ".json"):
            p = root / f"{workflow_key}{ext}"
            if p.is_file():
                return p
        raise WorkflowFileNotFound(f"Workflow not found: {root}/{workflow_key}")
    
    def _parse(self, filename: str, raw: str) -> Dict[str, Any]:
        if filename.endswith(".json"):
            return json.loads(raw)
        if filename.endswith((".yaml", ".yml")):
            data = yaml.safe_load(raw)
            if data is None:
                raise ValueError(f"Workflow file '{filename}' is empty")
            return data
        raise ValueError(f"Unsupported workflow file: {filename}")
    
    def _build_workflow_def(self, workflow_key: str, raw: Dict[str, Any]) -> "WorkflowDef":
        start = raw.get("start")
        if not start:
            raise ValueError(f"{workflow_key}: missing 'start'")

        raw_steps = raw.get("steps")
        if not isinstance(raw_steps, list) or not raw_steps:
            raise ValueError(f"{workflow_key}: 'steps' must be a non-empty list")

        steps: Dict[str, StepDef] = {}

        for s in raw_steps:
            sid = s.get("id")
            if not sid:
                raise ValueError(f"{workflow_key}: step without id")

            prompt = None
            if s.get("prompt") is not None:
                p = s["prompt"]
                prompt = PromptDef(
                    kind=p.get("kind", "text"),
                    title=p["title"],
                    var=p.get("var"),
                    required=bool(p.get("required", True)),
                )

            step = StepDef(
                id=sid,
                run=s.get("run"),
                prompt=prompt,
                next=s.get("next"),
                end=s.get("end"),
            )

            # Guardrail: exactly one of run/prompt/end
            actions = sum([step.run is not None, step.prompt is not None, step.end is not None])
            if actions != 1:
                raise ValueError(
                    f"{workflow_key}:{sid}: define exactly one of [run, prompt, end]"
                )

            steps[sid] = step

        if start not in steps:
            raise ValueError(f"{workflow_key}: start step '{start}' not found")

        return WorkflowDef(id=workflow_key, start=start, steps=steps)