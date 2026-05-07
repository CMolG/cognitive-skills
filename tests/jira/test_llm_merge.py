"""Tests for the LLM-augmented analysis merge."""

import json
from argparse import Namespace
from pathlib import Path

import jira_pipeline_cli as cli


def _write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload))


def test_merge_unions_list_fields(tmp_path):
    analysis_path = tmp_path / "analysis.json"
    suggestions_path = tmp_path / "suggestions.json"
    output_path = tmp_path / "merged.json"

    _write(analysis_path, {
        "schemaVersion": "1.0.0",
        "issueKey": "DEMO-1",
        "functionalEntities": ["user", "account"],
        "missingBusinessDecisions": ["scope"],
    })
    _write(suggestions_path, {
        "functionalEntities": ["partner", "user"],  # "user" duplicates
        "missingBusinessDecisions": ["expiration", "scope"],
    })

    rc = cli.merge_llm_suggestions(Namespace(
        analysis=str(analysis_path),
        suggestions=str(suggestions_path),
        output=str(output_path),
    ))
    assert rc == 0

    merged = json.loads(output_path.read_text())
    # Lists become sorted union (no duplicates)
    assert merged["functionalEntities"] == ["account", "partner", "user"]
    assert merged["missingBusinessDecisions"] == ["expiration", "scope"]
    assert merged["_llmAugmentation"]["acceptedKeys"] == [
        "functionalEntities",
        "missingBusinessDecisions",
    ]
    assert merged["_llmAugmentation"]["rejectedKeys"] == []
    # Provenance is captured
    snapshot = merged["_llmAugmentation"]["ruleBasedSnapshot"]
    assert snapshot["functionalEntities"] == ["user", "account"]


def test_merge_replaces_scalar_fields_and_keeps_provenance(tmp_path):
    analysis_path = tmp_path / "analysis.json"
    suggestions_path = tmp_path / "suggestions.json"

    _write(analysis_path, {
        "schemaVersion": "1.0.0",
        "issueKey": "DEMO-1",
        "businessGoal": "Reduce risk.",
    })
    _write(suggestions_path, {
        "businessGoal": "Comply with GDPR retention rules and reduce risk.",
    })

    cli.merge_llm_suggestions(Namespace(
        analysis=str(analysis_path),
        suggestions=str(suggestions_path),
        output=None,  # overwrite analysis in place
    ))

    merged = json.loads(analysis_path.read_text())
    assert merged["businessGoal"] == "Comply with GDPR retention rules and reduce risk."
    assert merged["_llmAugmentation"]["ruleBasedSnapshot"]["businessGoal"] == "Reduce risk."


def test_merge_rejects_unknown_keys(tmp_path):
    analysis_path = tmp_path / "analysis.json"
    suggestions_path = tmp_path / "suggestions.json"

    _write(analysis_path, {
        "schemaVersion": "1.0.0",
        "issueKey": "DEMO-1",
        "functionalEntities": [],
    })
    _write(suggestions_path, {
        "functionalEntities": ["user"],
        # Disallowed: would let the model rewrite immutable identity
        "issueKey": "DEMO-2",
        # Disallowed: arbitrary new field
        "secretInjection": "haha",
    })

    cli.merge_llm_suggestions(Namespace(
        analysis=str(analysis_path),
        suggestions=str(suggestions_path),
        output=str(analysis_path),
    ))

    merged = json.loads(analysis_path.read_text())
    # issueKey is silently skipped (immutable), secretInjection ends up in rejectedKeys
    assert merged["issueKey"] == "DEMO-1"
    assert "secretInjection" not in merged
    assert merged["_llmAugmentation"]["rejectedKeys"] == ["secretInjection"]


def test_merge_rejects_non_list_for_list_fields(tmp_path):
    analysis_path = tmp_path / "analysis.json"
    suggestions_path = tmp_path / "suggestions.json"

    _write(analysis_path, {
        "schemaVersion": "1.0.0",
        "issueKey": "DEMO-1",
        "functionalEntities": ["user"],
    })
    _write(suggestions_path, {
        "functionalEntities": "user, partner",  # wrong shape
    })

    cli.merge_llm_suggestions(Namespace(
        analysis=str(analysis_path),
        suggestions=str(suggestions_path),
        output=str(analysis_path),
    ))

    merged = json.loads(analysis_path.read_text())
    assert merged["functionalEntities"] == ["user"]  # untouched
    assert "functionalEntities" in merged["_llmAugmentation"]["rejectedKeys"]
