#!/usr/bin/env python3
"""Eval harness runner.

Reads task definitions from `evals/tasks/<task>/criteria.json`, scores
every output under `evals/results/<run-id>/<task>/<arm>.md`, and emits
a Markdown + JSON report under `evals/results/<run-id>/report.{md,json}`.

The harness is deterministic and stdlib-only. It never calls an LLM.
The "model" running each task is whatever the user invokes the skill
with; this script only checks the *outputs* against deterministic
criteria.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from statistics import mean, stdev
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
import scoring  # noqa: E402


SCHEMA_VERSION = "1.0.0"
ARMS = ["baseline", "ceet", "generic"]


def list_tasks(tasks_dir: Path) -> list[str]:
    return sorted(p.name for p in tasks_dir.iterdir() if p.is_dir() and (p / "criteria.json").exists())


def load_task(tasks_dir: Path, name: str) -> dict[str, Any]:
    criteria = json.loads((tasks_dir / name / "criteria.json").read_text(encoding="utf-8"))
    corpus_path = tasks_dir / name / "voice-corpus.txt"
    corpus = corpus_path.read_text(encoding="utf-8") if corpus_path.exists() else None
    return {"name": name, "criteria": criteria, "corpus": corpus}


def score_run(results_dir: Path, task: dict[str, Any]) -> dict[str, Any]:
    """Score every available arm for a task. Missing arms are skipped."""
    task_dir = results_dir / task["name"]
    arm_scores: dict[str, dict[str, Any]] = {}
    for arm in ARMS:
        output_path = task_dir / f"{arm}.md"
        if not output_path.exists():
            continue
        text = output_path.read_text(encoding="utf-8")
        arm_scores[arm] = scoring.score_output(text, task["criteria"], task["corpus"])
    return arm_scores


def deltas(arm_scores: dict[str, dict[str, Any]]) -> dict[str, float | None]:
    """ceet vs baseline composite delta, ceet vs generic composite delta."""
    if "ceet" not in arm_scores:
        return {"ceetMinusBaseline": None, "ceetMinusGeneric": None}
    ceet = arm_scores["ceet"]["compositeScore"]
    return {
        "ceetMinusBaseline": (
            round(ceet - arm_scores["baseline"]["compositeScore"], 4)
            if "baseline" in arm_scores else None
        ),
        "ceetMinusGeneric": (
            round(ceet - arm_scores["generic"]["compositeScore"], 4)
            if "generic" in arm_scores else None
        ),
    }


def render_markdown(report: dict[str, Any]) -> str:
    """Render the JSON report as a human-readable Markdown table."""
    lines = [f"# Eval report — {report['runId']}", ""]
    lines.append(f"> schemaVersion: `{report['schemaVersion']}`")
    lines.append(f"> tasks scored: {len(report['tasks'])}")
    lines.append("")
    lines.append("| Task | Arm | Words | Phrases | Sections | Voice | Composite |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for task_name, task_report in report["tasks"].items():
        for arm, scores in task_report["arms"].items():
            lines.append(
                f"| `{task_name}` | `{arm}` | {scores['wordCount']} | "
                f"{scores['phraseCoverage']:.2f} | {scores['sectionCoverage']:.2f} | "
                f"{scores['voiceAlignment'] if scores['voiceAlignment'] is not None else '—'} | "
                f"{scores['compositeScore']:.2f} |"
            )
    lines.append("")
    lines.append("## Deltas (ceet vs control arms)")
    lines.append("")
    lines.append("| Task | ceet − baseline | ceet − generic |")
    lines.append("|---|---:|---:|")
    for task_name, task_report in report["tasks"].items():
        d = task_report["deltas"]
        lines.append(
            f"| `{task_name}` | "
            f"{d['ceetMinusBaseline'] if d['ceetMinusBaseline'] is not None else '—'} | "
            f"{d['ceetMinusGeneric'] if d['ceetMinusGeneric'] is not None else '—'} |"
        )
    return "\n".join(lines) + "\n"


def aggregate(report: dict[str, Any]) -> dict[str, Any]:
    """Compute mean composite per arm across tasks for the release gate."""
    arm_composites: dict[str, list[float]] = {arm: [] for arm in ARMS}
    for task_report in report["tasks"].values():
        for arm, scores in task_report["arms"].items():
            arm_composites[arm].append(scores["compositeScore"])
    return {
        arm: {
            "mean": round(mean(values), 4) if values else None,
            "stdev": round(stdev(values), 4) if len(values) >= 2 else None,
            "n": len(values),
        }
        for arm, values in arm_composites.items()
    }


def run(run_id: str, tasks_dir: Path, results_root: Path) -> dict[str, Any]:
    results_dir = results_root / run_id
    if not results_dir.exists():
        raise SystemExit(f"results directory does not exist: {results_dir}")

    report: dict[str, Any] = {
        "schemaVersion": SCHEMA_VERSION,
        "runId": run_id,
        "tasks": {},
    }

    for task_name in list_tasks(tasks_dir):
        task = load_task(tasks_dir, task_name)
        arm_scores = score_run(results_dir, task)
        if not arm_scores:
            continue
        report["tasks"][task_name] = {
            "criteria": task["criteria"],
            "arms": arm_scores,
            "deltas": deltas(arm_scores),
        }

    report["aggregate"] = aggregate(report)

    (results_dir / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (results_dir / "report.md").write_text(render_markdown(report), encoding="utf-8")
    return report


def gate(report: dict[str, Any], min_delta: float = 0.05) -> tuple[bool, str]:
    """Release gate: ceet must beat baseline by `min_delta` on at least 2/3 tasks."""
    wins = 0
    for task_name, task_report in report["tasks"].items():
        delta = task_report["deltas"]["ceetMinusBaseline"]
        if delta is not None and delta >= min_delta:
            wins += 1
    total = len(report["tasks"])
    passed = total > 0 and wins >= max(1, math.ceil(total * 2 / 3))
    msg = (
        f"ceet beats baseline by ≥ {min_delta} on {wins} of {total} tasks; "
        f"gate {'passed' if passed else 'failed'}"
    )
    return passed, msg


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the cognitive-skills eval harness.")
    parser.add_argument("--run-id", required=True, help="Subfolder under evals/results/.")
    parser.add_argument("--tasks-dir", default=str(REPO_ROOT / "evals" / "tasks"))
    parser.add_argument("--results-dir", default=str(REPO_ROOT / "evals" / "results"))
    parser.add_argument("--gate", action="store_true", help="Exit non-zero if ceet doesn't beat baseline.")
    parser.add_argument("--min-delta", type=float, default=0.05, help="Minimum composite delta for the gate.")
    args = parser.parse_args()

    report = run(args.run_id, Path(args.tasks_dir), Path(args.results_dir))
    print(f"report written to evals/results/{args.run_id}/report.{{json,md}}")

    if args.gate:
        passed, msg = gate(report, min_delta=args.min_delta)
        print(msg)
        return 0 if passed else 1
    return 0


# Local import here to avoid a top-level math import shadow.
import math  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
