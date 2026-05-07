"""Tests for ceet-sub-agent-orchestration/scripts/validate_handoff.py."""

import validate_handoff


VALID_PLAN = {
    "schemaVersion": "1.0.0",
    "planId": "plan-1",
    "goal": "Audit checkout flow",
    "tasks": [
        {
            "id": "T1",
            "role": "ceet-backend-engineer",
            "scope": "Audit migration plan",
            "expectedArtifacts": ["report"],
            "dependsOn": [],
        },
        {
            "id": "T2",
            "role": "ceet-devops-sre",
            "scope": "Add alerts",
            "expectedArtifacts": ["diff"],
            "dependsOn": ["T1"],
        },
    ],
}


VALID_RESULT = {
    "schemaVersion": "1.0.0",
    "planId": "plan-1",
    "taskId": "T1",
    "role": "ceet-backend-engineer",
    "status": "completed",
    "artifacts": [{"path": "report.md", "kind": "report"}],
    "summary": "ok",
}


def test_valid_plan_has_no_errors():
    assert validate_handoff.validate_plan(VALID_PLAN) == []


def test_plan_rejects_wrong_schema_version():
    plan = dict(VALID_PLAN, schemaVersion="0.9.0")
    errors = validate_handoff.validate_plan(plan)
    assert any("schemaVersion" in e for e in errors)


def test_plan_rejects_duplicate_task_ids():
    plan = dict(VALID_PLAN)
    plan["tasks"] = [
        {**VALID_PLAN["tasks"][0]},
        {**VALID_PLAN["tasks"][0]},  # same id "T1"
    ]
    errors = validate_handoff.validate_plan(plan)
    assert any("duplicate id" in e for e in errors)


def test_plan_rejects_forward_dependencies():
    plan = dict(VALID_PLAN)
    plan["tasks"] = [
        {
            "id": "T1",
            "role": "ceet-backend-engineer",
            "scope": "x",
            "expectedArtifacts": ["report"],
            "dependsOn": ["T2"],  # forward
        },
        {
            "id": "T2",
            "role": "ceet-devops-sre",
            "scope": "y",
            "expectedArtifacts": ["diff"],
            "dependsOn": [],
        },
    ]
    errors = validate_handoff.validate_plan(plan)
    assert any("not declared before" in e for e in errors)


def test_plan_rejects_empty_task_list():
    plan = dict(VALID_PLAN, tasks=[])
    errors = validate_handoff.validate_plan(plan)
    assert any("non-empty list" in e for e in errors)


def test_valid_result_has_no_errors():
    assert validate_handoff.validate_result(VALID_RESULT) == []


def test_result_completed_requires_artifacts():
    result = dict(VALID_RESULT, artifacts=[])
    errors = validate_handoff.validate_result(result)
    assert any("non-empty when status=completed" in e for e in errors)


def test_result_failed_requires_error():
    result = {**VALID_RESULT, "status": "failed", "artifacts": []}
    errors = validate_handoff.validate_result(result)
    assert any("error" in e for e in errors)


def test_result_rejects_unknown_artifact_kind():
    result = dict(VALID_RESULT, artifacts=[{"path": "x.md", "kind": "wat"}])
    errors = validate_handoff.validate_result(result)
    assert any("file|diff|report|decision" in e for e in errors)


def test_result_rejects_unknown_status():
    result = dict(VALID_RESULT, status="in-progress")
    errors = validate_handoff.validate_result(result)
    assert any("completed|failed|skipped" in e for e in errors)
