"""Snapshot-style tests that pin the full pipeline output for each fixture.

To regenerate the stored snapshots after an intentional contract change,
run with `SNAPSHOT_UPDATE=1 pytest tests/jira/test_pipeline_snapshots.py`.
"""

import json
import os
from argparse import Namespace
from datetime import datetime, timezone
from pathlib import Path

import pytest

import jira_pipeline_cli as cli


FIXTURES = Path(__file__).parent / "fixtures"
SNAPSHOTS = Path(__file__).parent / "snapshots"

SCENARIOS = ["tight", "medium", "empty", "ambiguous"]

VOLATILE_KEYS = {"fetchedAt", "generatedAt", "resolvedAt", "lastUpdated", "capturedAt"}


def _strip_volatile(node):
    """Recursively replace timestamp-like fields with a placeholder so snapshots are stable."""
    if isinstance(node, dict):
        return {k: ("<timestamp>" if k in VOLATILE_KEYS else _strip_volatile(v)) for k, v in node.items()}
    if isinstance(node, list):
        return [_strip_volatile(item) for item in node]
    return node


def _run_full_pipeline(fixture_path: Path, tmp_path: Path) -> dict[str, dict]:
    issue_path = tmp_path / "issue.json"
    issue_path.write_text(fixture_path.read_text())

    analysis_path = tmp_path / "analysis.json"
    cli.discovery(Namespace(input=str(issue_path), output=str(analysis_path)))

    questions_path = tmp_path / "questions.json"
    cli.generate_questions(
        Namespace(
            input=str(analysis_path),
            output=str(questions_path),
            baseline_budget=cli.DEFAULT_BASELINE_BUDGET,
            signal_budget=cli.DEFAULT_SIGNAL_BUDGET,
        )
    )

    # Synthesize deterministic answers so resolve-contract can produce a contract.
    questions = json.loads(questions_path.read_text())
    state = {
        "issueKey": questions["issueKey"],
        "answers": {
            q["id"]: {
                "answer": f"Decision for {q['category']}",
                "capturedAt": datetime.now(timezone.utc).isoformat(),
                "priority": q["priority"],
                "category": q["category"],
            }
            for q in questions["questions"]
        },
        "lastUpdated": datetime.now(timezone.utc).isoformat(),
    }
    state_path = tmp_path / "state.json"
    state_path.write_text(json.dumps(state))

    contract_path = tmp_path / "contract.json"
    cli.resolve_contract(
        Namespace(
            questions=str(questions_path),
            answers=str(state_path),
            output=str(contract_path),
        )
    )

    plan_path = tmp_path / "plan.json"
    cli.base_branch_plan(
        Namespace(
            analysis=str(analysis_path),
            contract=str(contract_path),
            output=str(plan_path),
        )
    )

    return {
        "analysis": json.loads(analysis_path.read_text()),
        "questions": json.loads(questions_path.read_text()),
        "contract": json.loads(contract_path.read_text()),
        "plan": json.loads(plan_path.read_text()),
    }


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_pipeline_snapshot(scenario, tmp_path):
    fixture = FIXTURES / f"issue_{scenario}.json"
    snapshot_dir = SNAPSHOTS / scenario
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    outputs = _run_full_pipeline(fixture, tmp_path)
    cleaned = {name: _strip_volatile(payload) for name, payload in outputs.items()}

    if os.environ.get("SNAPSHOT_UPDATE") == "1":
        for name, payload in cleaned.items():
            (snapshot_dir / f"{name}.json").write_text(
                json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
            )
        return

    for name, actual in cleaned.items():
        snap_file = snapshot_dir / f"{name}.json"
        assert snap_file.exists(), (
            f"missing snapshot {snap_file}; regenerate with SNAPSHOT_UPDATE=1"
        )
        expected = json.loads(snap_file.read_text())
        assert actual == expected, f"snapshot mismatch for {scenario}/{name}"


@pytest.mark.parametrize(
    "scenario,expected_level,expected_status",
    [
        ("tight", "LOW", "READY_FOR_BASE_BRANCH"),
        ("medium", "MEDIUM", "PLAN_ONLY"),
        ("empty", "HIGH", "QUESTIONS_ONLY"),
        ("ambiguous", "HIGH", "QUESTIONS_ONLY"),
    ],
)
def test_pipeline_status_matches_scenario(scenario, expected_level, expected_status, tmp_path):
    fixture = FIXTURES / f"issue_{scenario}.json"
    outputs = _run_full_pipeline(fixture, tmp_path)
    assert outputs["analysis"]["ambiguityLevel"]["level"] == expected_level
    assert outputs["plan"]["status"] == expected_status


def test_contract_preserves_unmapped_answers(tmp_path):
    fixture = FIXTURES / "issue_tight.json"
    outputs = _run_full_pipeline(fixture, tmp_path)
    contract = outputs["contract"]
    assert "unmappedAnswers" in contract
    assert isinstance(contract["unmappedAnswers"], list)


def test_plan_uses_proposed_branch_name(tmp_path):
    fixture = FIXTURES / "issue_tight.json"
    outputs = _run_full_pipeline(fixture, tmp_path)
    plan = outputs["plan"]
    assert "proposedBranchName" in plan
    assert "branchName" not in plan
    assert plan["proposedBranchName"].startswith("ai/")


def test_all_artifacts_carry_schema_version(tmp_path):
    fixture = FIXTURES / "issue_tight.json"
    outputs = _run_full_pipeline(fixture, tmp_path)
    for name, payload in outputs.items():
        assert payload.get("schemaVersion") == cli.CONTRACT_SCHEMA_VERSION, (
            f"{name} missing schemaVersion"
        )
