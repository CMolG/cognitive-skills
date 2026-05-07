"""Tests for evals/scripts/run.py."""

import json
from pathlib import Path

import run as eval_run


REPO_ROOT = Path(__file__).resolve().parents[2]
TASKS_DIR = REPO_ROOT / "evals" / "tasks"
RESULTS_DIR = REPO_ROOT / "evals" / "results"


def test_seed_run_produces_report_and_meaningful_deltas():
    """The seed run must produce a report where ceet beats baseline on 2/3 tasks."""
    report = eval_run.run("seed-2026-05-07", TASKS_DIR, RESULTS_DIR)

    # All three tasks scored
    assert set(report["tasks"]) == {
        "engineering-pr-review",
        "product-prd-draft",
        "copy-headlines",
    }

    # ceet beats baseline on at least 2/3 tasks (release gate)
    wins = sum(
        1
        for task in report["tasks"].values()
        if task["deltas"]["ceetMinusBaseline"] is not None
        and task["deltas"]["ceetMinusBaseline"] > 0
    )
    assert wins >= 2

    # Report files written
    assert (RESULTS_DIR / "seed-2026-05-07" / "report.json").exists()
    assert (RESULTS_DIR / "seed-2026-05-07" / "report.md").exists()


def test_gate_passes_for_seed():
    report = eval_run.run("seed-2026-05-07", TASKS_DIR, RESULTS_DIR)
    passed, msg = eval_run.gate(report, min_delta=0.05)
    assert passed, msg


def test_aggregate_includes_means():
    report = eval_run.run("seed-2026-05-07", TASKS_DIR, RESULTS_DIR)
    aggregate = report["aggregate"]
    assert aggregate["ceet"]["mean"] is not None
    assert aggregate["baseline"]["mean"] is not None
    # ceet mean composite should beat baseline mean composite
    assert aggregate["ceet"]["mean"] > aggregate["baseline"]["mean"]


def test_run_skips_tasks_without_outputs(tmp_path):
    """If a results directory has no arm files, the task is skipped silently."""
    results_root = tmp_path / "results"
    (results_root / "empty-run" / "engineering-pr-review").mkdir(parents=True)
    # No baseline.md / ceet.md / generic.md inside

    report = eval_run.run("empty-run", TASKS_DIR, results_root)
    assert report["tasks"] == {}


def test_run_id_must_exist():
    import pytest

    with pytest.raises(SystemExit):
        eval_run.run("nonexistent-run-id", TASKS_DIR, RESULTS_DIR)
