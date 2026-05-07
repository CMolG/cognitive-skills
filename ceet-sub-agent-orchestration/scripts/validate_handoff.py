#!/usr/bin/env python3
"""Validate orchestration handoff artifacts against the documented schemas.

This script enforces the `OrchestrationPlan` and `SubAgentResult`
contracts. The orchestrator skill calls it before dispatching work
(plan validation) and again after every sub-agent returns (result
validation), so a malformed payload fails fast and never propagates.

Usage:
    python3 validate_handoff.py --plan plan.json
    python3 validate_handoff.py --result result.json
    python3 validate_handoff.py --plan plan.json --results r1.json r2.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0.0"


def _require(path: str, condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(f"{path}: {message}")


def validate_plan(plan: dict[str, Any]) -> list[str]:
    """Return a list of human-readable schema violations (empty if valid)."""
    errors: list[str] = []
    _require("schemaVersion", plan.get("schemaVersion") == SCHEMA_VERSION,
             f"must equal '{SCHEMA_VERSION}'", errors)
    _require("planId", isinstance(plan.get("planId"), str) and plan["planId"],
             "must be a non-empty string", errors)
    _require("goal", isinstance(plan.get("goal"), str) and plan["goal"],
             "must be a non-empty string", errors)

    tasks = plan.get("tasks")
    _require("tasks", isinstance(tasks, list) and len(tasks) > 0,
             "must be a non-empty list", errors)

    if isinstance(tasks, list):
        ids: set[str] = set()
        for index, task in enumerate(tasks):
            base = f"tasks[{index}]"
            if not isinstance(task, dict):
                errors.append(f"{base}: must be an object")
                continue
            tid = task.get("id")
            _require(f"{base}.id", isinstance(tid, str) and tid, "must be a non-empty string", errors)
            if tid:
                if tid in ids:
                    errors.append(f"{base}.id: duplicate id '{tid}'")
                ids.add(tid)
            _require(f"{base}.role", isinstance(task.get("role"), str) and task["role"],
                     "must be a non-empty string", errors)
            _require(f"{base}.scope", isinstance(task.get("scope"), str) and task["scope"],
                     "must be a non-empty string", errors)
            _require(f"{base}.expectedArtifacts",
                     isinstance(task.get("expectedArtifacts"), list) and task["expectedArtifacts"],
                     "must be a non-empty list", errors)
            deps = task.get("dependsOn", [])
            _require(f"{base}.dependsOn", isinstance(deps, list),
                     "must be a list", errors)
            if isinstance(deps, list):
                for dep in deps:
                    if dep not in ids and dep != tid:
                        # Note: backward refs only; forward deps are flagged.
                        errors.append(f"{base}.dependsOn: '{dep}' not declared before this task")

    return errors


def validate_result(result: dict[str, Any]) -> list[str]:
    """Return a list of human-readable schema violations (empty if valid)."""
    errors: list[str] = []
    _require("schemaVersion", result.get("schemaVersion") == SCHEMA_VERSION,
             f"must equal '{SCHEMA_VERSION}'", errors)
    _require("planId", isinstance(result.get("planId"), str) and result["planId"],
             "must be a non-empty string", errors)
    _require("taskId", isinstance(result.get("taskId"), str) and result["taskId"],
             "must be a non-empty string", errors)
    _require("role", isinstance(result.get("role"), str) and result["role"],
             "must be a non-empty string", errors)

    status = result.get("status")
    _require("status", status in {"completed", "failed", "skipped"},
             "must be one of completed|failed|skipped", errors)

    artifacts = result.get("artifacts", [])
    _require("artifacts", isinstance(artifacts, list),
             "must be a list", errors)
    if status == "completed":
        _require("artifacts", isinstance(artifacts, list) and len(artifacts) > 0,
                 "must be non-empty when status=completed", errors)

    if status == "failed":
        _require("error", isinstance(result.get("error"), str) and result["error"],
                 "must be a non-empty string when status=failed", errors)

    if isinstance(artifacts, list):
        for index, artifact in enumerate(artifacts):
            base = f"artifacts[{index}]"
            if not isinstance(artifact, dict):
                errors.append(f"{base}: must be an object")
                continue
            _require(f"{base}.path", isinstance(artifact.get("path"), str) and artifact["path"],
                     "must be a non-empty string", errors)
            _require(f"{base}.kind", artifact.get("kind") in {"file", "diff", "report", "decision"},
                     "must be one of file|diff|report|decision", errors)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate orchestration handoff artifacts.")
    parser.add_argument("--plan", help="Path to an OrchestrationPlan JSON file.")
    parser.add_argument(
        "--result", "--results",
        dest="results",
        nargs="+",
        default=None,
        help="One or more SubAgentResult JSON files to validate.",
    )
    args = parser.parse_args()

    if not args.plan and not args.results:
        parser.error("provide at least --plan or --result")

    failures = 0

    if args.plan:
        plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
        errors = validate_plan(plan)
        if errors:
            failures += 1
            print(f"plan {args.plan}: invalid", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)
        else:
            print(f"plan {args.plan}: ok")

    if args.results:
        for path in args.results:
            result = json.loads(Path(path).read_text(encoding="utf-8"))
            errors = validate_result(result)
            if errors:
                failures += 1
                print(f"result {path}: invalid", file=sys.stderr)
                for err in errors:
                    print(f"  - {err}", file=sys.stderr)
            else:
                print(f"result {path}: ok")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
