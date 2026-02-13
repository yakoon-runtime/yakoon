from __future__ import annotations

import re
import json
import yaml
import importlib.resources as ir

from typing import Any, Dict
from yakoon.base.descriptors.workflow import WorkflowSource
from yakoon.base.models.workflow import PromptDef, StepDef, SwitchDef, WorkflowDef


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
        root = (
            ir.files(source.package) / source.workflow_path / source.workflow_sub_path
        )
        if not root.is_dir():
            raise WorkflowFileNotFound(f"Workflow directory not found: {root}")

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

    def _build_workflow_def(
        self, workflow_key: str, raw: Dict[str, Any]
    ) -> "WorkflowDef":
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

            # switch
            switch = None
            raw_switch = s.get("switch")
            if raw_switch is not None:
                if not isinstance(raw_switch, dict):
                    raise ValueError(f"Step '{sid}': switch must be a mapping")

                expr = raw_switch.get("expr")
                cases = raw_switch.get("cases")
                default = raw_switch.get("default")

                if not expr or not isinstance(expr, str):
                    raise ValueError(
                        f"Step '{sid}': switch.expr must be a non-empty string"
                    )

                if not isinstance(cases, dict) or not cases:
                    raise ValueError(
                        f"Step '{sid}': switch.cases must be a non-empty mapping"
                    )

                # normalize case keys
                norm_cases = {str(k).strip().lower(): v for k, v in cases.items()}

                if default is not None and not isinstance(default, str):
                    raise ValueError(f"Step '{sid}': switch.default must be a string")

                switch = SwitchDef(expr=expr, cases=norm_cases, default=default)

            # prompt
            prompt = None
            if s.get("prompt") is not None:
                p = s["prompt"]
                kind = p.get("kind") or p.get("type") or "text"

                if kind not in {
                    "text",
                    "select",
                    "confirm",
                    "review",
                }:  # review wenn ihr’s schon drin habt
                    raise ValueError(f"Unknown prompt kind: {kind}")

                options = p.get("options") or []
                default = p.get("default")

                # Guards für select
                if kind == "select":
                    if not isinstance(options, list) or not options:
                        raise ValueError(
                            f"Prompt '{sid}': select requires non-empty 'options'"
                        )
                    for opt in options:
                        if (
                            not isinstance(opt, dict)
                            or "label" not in opt
                            or "value" not in opt
                        ):
                            raise ValueError(
                                f"Prompt '{sid}': each option must have label/value"
                            )
                    # unique values
                    vals = [str(opt["value"]) for opt in options]
                    if len(vals) != len(set(vals)):
                        raise ValueError(
                            f"Prompt '{sid}': option values must be unique"
                        )
                    if default is not None and str(default) not in set(vals):
                        raise ValueError(
                            f"Prompt '{sid}': default '{default}' not in option values"
                        )

                # Guards für confirm
                if kind == "confirm":
                    if p.get("var") is None:
                        # confirm ohne var wäre sinnlos für Workflows; wenn ihr nur "ack" wollt, dann anders modellieren
                        raise ValueError(f"Prompt '{sid}': confirm requires 'var'")

                prompt = PromptDef(
                    kind=kind,
                    title=p["title"],
                    var=p.get("var"),
                    required=bool(p.get("required", True)),
                    options=options if kind == "select" else [],
                    default=default if kind == "select" else None,
                )

            branch = s.get("branch")
            if branch is not None:
                if not isinstance(branch, dict):
                    raise ValueError(f"Step '{sid}': branch must be a mapping")
                # normalize keys to lowercase strings
                branch = {str(k).strip().lower(): v for k, v in branch.items()}

            step = StepDef(
                id=sid,
                run=s.get("run"),
                prompt=prompt,
                next=s.get("next"),
                branch=branch,
                switch=switch,
                end=s.get("end"),
            )

            # Guardrail: exactly one of run/prompt/end
            actions = sum(
                [
                    step.run is not None,
                    step.prompt is not None,
                    step.switch is not None,
                    step.end is not None,
                ]
            )
            if actions != 1:
                raise ValueError(
                    f"{workflow_key}:{sid}: define exactly one of [run, prompt, switch, end]"
                )

            steps[sid] = step

        if start not in steps:
            raise ValueError(f"{workflow_key}: start step '{start}' not found")

        step_ids = set(steps.keys())
        for step in steps.values():
            if step.next and step.next not in step_ids:
                raise ValueError(
                    f"{workflow_key}:{step.id}: next target '{step.next}' not found"
                )

            if step.branch:
                for k, target in step.branch.items():
                    if target not in step_ids:
                        raise ValueError(
                            f"{workflow_key}:{step.id}: branch target '{target}' not found"
                        )

            if step.switch:
                for k, target in step.switch.cases.items():
                    if target not in step_ids:
                        raise ValueError(
                            f"{workflow_key}:{step.id}: switch case '{k}' target '{target}' not found"
                        )
                if step.switch.default and step.switch.default not in step_ids:
                    raise ValueError(
                        f"{workflow_key}:{step.id}: switch default target '{step.switch.default}' not found"
                    )

        return WorkflowDef(id=workflow_key, start=start, steps=steps)
